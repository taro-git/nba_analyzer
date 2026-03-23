import dayjs from "dayjs";
import { useEffect, useRef, useState } from "react";
import { useSearchParams } from "react-router";
import "swiper/css";
import { Swiper, type SwiperClass, SwiperSlide } from "swiper/react";

import { gameSummariesApi } from "../api/gameSummaries.api";
import GameCard from "../components/GameCard";
import SwipeCalendar, { QueryParameterKeysOfSwipeCalendar } from "../components/SwipeCalendar";
import { Date } from "../types/date";
import { GameStatus, type GameSummary } from "../types/gameSummaries";
import { type Route } from "./+types/games";

function getDateFromQueryParameter(params: URLSearchParams): Date {
  const param = params.get(QueryParameterKeysOfSwipeCalendar.GameDate);
  const date = new Date();
  if (param != null) {
    date.date = dayjs(param);
  }
  return date;
}

const SLIDES_RANGE = 3;

type Response = {
  games: GameSummary[];
  date: Date;
};

/**
 * Games 画面のクライアントローダーを定義します.
 */
export async function clientLoader({ request }: Route.ClientLoaderArgs): Promise<Response> {
  const date = getDateFromQueryParameter(new URLSearchParams(new URL(request.url).search));
  const games = await gameSummariesApi.get({
    from_utc: date.getAddedUtcIso(-SLIDES_RANGE),
    to_utc: date.getAddedUtcIso(SLIDES_RANGE),
  });
  return { games, date };
}

/**
 * Games 画面を定義します.
 */
export default function Games({ loaderData }: Route.ComponentProps) {
  // ----------------------------------------------------------------------
  // Initial
  // ----------------------------------------------------------------------
  const startEpoch = new Date(dayjs("1983-10-01")).getAddedEpochSec();
  const today = dayjs();
  const endEpoch = new Date(
    today.month() <= 8 ? dayjs(`${today.year()}-09-30`) : dayjs(`${today.year() + 1}-09-30`),
  ).getAddedEpochSec();

  // ----------------------------------------------------------------------
  // Loadings
  // ----------------------------------------------------------------------
  const games = loaderData.games;

  // ----------------------------------------------------------------------
  // States
  // ----------------------------------------------------------------------
  const [searchParams, setSearchParams] = useSearchParams();
  const [selectedDate, setSelectedDate] = useState<Date>(getDateFromQueryParameter(searchParams));
  const [swiper, setSwiper] = useState<SwiperClass | null>(null);

  // ----------------------------------------------------------------------
  // Refs
  // ----------------------------------------------------------------------
  const activeSlideIndex = useRef<number>(SLIDES_RANGE);
  const isSlideReset = useRef<boolean>(false);
  const scrollRefs = useRef<(HTMLDivElement | null)[]>([]);

  // ----------------------------------------------------------------------
  // Events
  // ----------------------------------------------------------------------
  useEffect(() => {
    if (getDateFromQueryParameter(searchParams).getAddedEpochSec() === selectedDate.getAddedEpochSec()) return;
    setSearchParams(
      (prev) => {
        const next = new URLSearchParams(prev);
        next.set(QueryParameterKeysOfSwipeCalendar.GameDate, selectedDate.getAddedDateString());
        return next;
      },
      { replace: true },
    );
  }, [selectedDate]);

  const resetSlide = () => {
    if (!swiper) return;
    isSlideReset.current = true;
    swiper.slideTo(SLIDES_RANGE, 0);
    activeSlideIndex.current = SLIDES_RANGE;
    isSlideReset.current = false;
  };

  useEffect(() => {
    resetSlide();
    if (loaderData.date.getAddedEpochSec() !== selectedDate.getAddedEpochSec()) {
      setSelectedDate(loaderData.date);
    }
  }, [loaderData]);

  const onSlideChange = (swiper: SwiperClass) => {
    const index = swiper.activeIndex;
    if (index === activeSlideIndex.current || isSlideReset.current) return;
    const newDate = new Date(selectedDate.getAddedDayjs(index > activeSlideIndex.current ? 1 : -1));
    if (newDate.getAddedEpochSec() > endEpoch || newDate.getAddedEpochSec() < startEpoch) {
      resetSlide();
      return;
    }
    scrollRefs.current.forEach((el, i) => {
      if (i !== index && el) {
        el.scrollTop = 0;
      }
    });
    activeSlideIndex.current = index;
    setSelectedDate(newDate);
  };

  // ----------------------------------------------------------------------
  // Views
  // ----------------------------------------------------------------------
  const gameStatusSequense = {
    [GameStatus.Live]: 0,
    [GameStatus.Scheduled]: 1,
    [GameStatus.Final]: 2,
  };
  const gamesByDate = Array.from({ length: 2 * SLIDES_RANGE + 1 }, (_, i) => i - SLIDES_RANGE).map((i) => {
    return games
      .filter((game) => {
        const date = getDateFromQueryParameter(searchParams);
        const epoc = game.startDatetime.unix();
        return epoc >= date.getAddedEpochSec(i) && epoc < date.getAddedEpochSec(i + 1);
      })
      .sort((a, b) => {
        if (a.status !== b.status) {
          return gameStatusSequense[a.status] - gameStatusSequense[b.status];
        } else {
          if (a.startDatetime.unix() !== b.startDatetime.unix()) {
            return a.startDatetime.unix() - b.startDatetime.unix();
          } else {
            return a.gameId.localeCompare(b.gameId);
          }
        }
      });
  });

  return (
    <>
      <SwipeCalendar selectedDate={selectedDate} setSelectedDate={setSelectedDate} />
      <Swiper
        style={{ zIndex: 0 }}
        centeredSlides={true}
        centeredSlidesBounds={true}
        slidesPerView={1}
        spaceBetween={0}
        initialSlide={activeSlideIndex.current}
        onSwiper={(swiper) => setSwiper(swiper)}
        onSlideChange={onSlideChange}
      >
        {gamesByDate.map((games, index) => {
          return (
            <SwiperSlide key={index}>
              <div
                ref={(el) => {
                  scrollRefs.current[index] = el;
                }}
                style={{
                  height: "calc(100dvh - 11rem)",
                  width: "100%",
                  overflowY: "auto",
                  display: "grid",
                  justifyItems: "center",
                  alignContent: "start",
                }}
              >
                {games.map((game) => {
                  return <GameCard key={game.gameId} gameSummary={game} />;
                })}
                {games.length === 0 && <div style={{ padding: "2rem", fontSize: "3rem" }}>No Games</div>}
              </div>
            </SwiperSlide>
          );
        })}
      </Swiper>
    </>
  );
}
