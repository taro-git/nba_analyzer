import { CalendarMonth, Refresh } from "@mui/icons-material";
import { Avatar, Dialog, Grid, IconButton, useColorScheme } from "@mui/material";
import { AdapterDayjs } from "@mui/x-date-pickers/AdapterDayjs";
import { DateCalendar } from "@mui/x-date-pickers/DateCalendar";
import { LocalizationProvider } from "@mui/x-date-pickers/LocalizationProvider";

import dayjs, { type Dayjs } from "dayjs";
import { useEffect, useMemo, useRef, useState } from "react";
import { useSearchParams } from "react-router";
import "swiper/css";
import { Virtual } from "swiper/modules";
import { Swiper, type SwiperClass, SwiperSlide } from "swiper/react";

import { theme } from "../routes/layout";
import { Date, Day } from "../types/date";
import "./styles.css";

/**
 * カレンダーコンポーネントで使用するクエリパラメータのキーを定義します.
 */
export const QueryParameterKeysOfSwipeCalendar = {
  GameDate: "game-date",
} as const;

/**
 * カレンダーコンポーネントで使用するクエリパラメータのキーを定義します.
 */
export type QueryParameterKeysOfSwipeCalendar =
  (typeof QueryParameterKeysOfSwipeCalendar)[keyof typeof QueryParameterKeysOfSwipeCalendar];

function getDaysFromStartByQueryParameter(start: Dayjs, searchParams: URLSearchParams): number {
  const param = searchParams.get(QueryParameterKeysOfSwipeCalendar.GameDate);
  if (param == null) {
    return dayjs().diff(start, "day");
  }
  return dayjs(searchParams.get(QueryParameterKeysOfSwipeCalendar.GameDate)).diff(start, "day");
}

/**
 * nba_analyzer 向けのカレンダーコンポーネントです.
 */
export default function SwipeCalendar() {
  // ----------------------------------------------------------------------
  // Initialization
  // ----------------------------------------------------------------------
  const start = dayjs("1970-10-01");
  const today = dayjs();
  const end = today.month() <= 8 ? dayjs(`${today.year()}-09-30`) : dayjs(`${today.year() + 1}-09-30`);
  const startDate = new Date(start);
  const daysFromCenterToVisibleEdge = 61;

  // ----------------------------------------------------------------------
  // States
  // ----------------------------------------------------------------------
  const [searchParams, setSearchParams] = useSearchParams();
  const initialDaysFromStart = getDaysFromStartByQueryParameter(start, searchParams);
  const [daysFromStartToVisibleBeginning, setDaysFromStartToVisibleBeginning] = useState(
    initialDaysFromStart - daysFromCenterToVisibleEdge,
  );
  const [daysFromStartToVisibleEnd, setDaysFromStartToVisibleEnd] = useState(
    initialDaysFromStart + daysFromCenterToVisibleEdge,
  );
  const [selectedDaysFromStart, setSelectedDaysFromStart] = useState<number>(initialDaysFromStart);
  const [centeredDaysFromStart, setCenteredDaysFromStart] = useState<number>(initialDaysFromStart);
  const [calendarOpen, setCalendarOpen] = useState(false);
  const [calendarValue, setCalendarValue] = useState(startDate.getAddedDayjs(selectedDaysFromStart));
  const visibleDaysFromStart = useMemo(() => {
    return Array.from(
      { length: Math.min(end.diff(start, "day"), daysFromStartToVisibleEnd) - daysFromStartToVisibleBeginning + 1 },
      (_, i) => daysFromStartToVisibleBeginning + i,
    );
  }, [daysFromStartToVisibleBeginning, daysFromStartToVisibleEnd]);
  const swiperRef = useRef<SwiperClass | null>(null);

  // ----------------------------------------------------------------------
  // Events
  // ----------------------------------------------------------------------
  useEffect(() => {
    const days = getDaysFromStartByQueryParameter(start, searchParams);
    if (days !== selectedDaysFromStart) {
      dateChange(days);
    }
  }, [searchParams]);

  const dateChange = (daysFromStart: number) => {
    setSelectedDaysFromStart(daysFromStart);
    const nextBeginning = Math.max(0, daysFromStart - daysFromCenterToVisibleEdge);
    setDaysFromStartToVisibleBeginning(nextBeginning);
    setDaysFromStartToVisibleEnd(daysFromStart + daysFromCenterToVisibleEdge);
    centeringDate(nextBeginning == 0 ? daysFromStart : daysFromCenterToVisibleEdge);
    setCenteredDaysFromStart(daysFromStart);
    setSearchParams(
      (prev) => {
        prev.set(QueryParameterKeysOfSwipeCalendar.GameDate, startDate.getAddedDateString(daysFromStart));
        return prev;
      },
      { replace: true },
    );
    setCalendarValue(startDate.getAddedDayjs(daysFromStart));
  };

  const centeringDate = (index: number) => {
    if (swiperRef.current != null) {
      swiperRef.current.slideTo(index, 0);
    }
  };

  const onReachBeginning = () => {
    if (!swiperRef.current) return;

    const swiper = swiperRef.current;
    swiper.allowTouchMove = false;
    swiper.allowSlideNext = false;
    swiper.allowSlidePrev = false;
    const currentIndex = swiper.activeIndex;
    const prevBeginning = daysFromStartToVisibleBeginning;

    const nextBeginning = Math.max(0, prevBeginning - daysFromCenterToVisibleEdge);

    setDaysFromStartToVisibleBeginning(nextBeginning);

    requestAnimationFrame(() => {
      requestAnimationFrame(() => {
        centeringDate(currentIndex + prevBeginning - nextBeginning);
      });
    });
    swiper.allowTouchMove = true;
    swiper.allowSlideNext = true;
    swiper.allowSlidePrev = true;
  };

  // ----------------------------------------------------------------------
  // Views
  // ----------------------------------------------------------------------
  const systemMode = useColorScheme().systemMode;
  const palette = useMemo(() => {
    return systemMode === "light" ? theme.colorSchemes.light?.palette : theme.colorSchemes.dark?.palette;
  }, [systemMode]);

  return (
    <>
      <Grid container spacing={0} sx={{ bgcolor: palette?.background?.paper, padding: 1 }}>
        <Grid display="flex" justifyContent="center" alignItems="center" size={2}>
          <IconButton
            sx={{
              color: palette?.text?.primary,
              borderColor: palette?.text?.primary,
              "&:hover": {
                color: palette?.primary?.main,
                borderColor: palette?.primary?.main,
              },
              fontSize: "1rem",
            }}
            onClick={() => dateChange(today.diff(start, "day"))}
          >
            <Refresh />
          </IconButton>
        </Grid>
        <Grid display="flex" justifyContent="center" alignItems="center" size="grow" fontSize="1.5rem">
          {`${startDate.getAddedYear(centeredDaysFromStart)}/${startDate.getAddedMonth(centeredDaysFromStart)}`}
        </Grid>
        <Grid display="flex" justifyContent="center" alignItems="center" size={2}>
          <LocalizationProvider dateAdapter={AdapterDayjs}>
            <IconButton
              sx={{
                color: palette?.text?.primary,
                borderColor: palette?.text?.primary,
                "&:hover": {
                  color: palette?.primary?.main,
                  borderColor: palette?.primary?.main,
                },
                fontSize: "1rem",
              }}
              onClick={() => setCalendarOpen(true)}
            >
              <CalendarMonth />
            </IconButton>

            <Dialog open={calendarOpen} onClose={() => setCalendarOpen(false)}>
              <DateCalendar
                value={calendarValue}
                minDate={start}
                maxDate={end}
                onChange={(newValue) => {
                  if (newValue != null) {
                    dateChange(newValue.diff(start, "day"));
                    setCalendarOpen(false);
                  }
                }}
              />
            </Dialog>
          </LocalizationProvider>
        </Grid>
      </Grid>
      <Grid container spacing={0} sx={{ bgcolor: palette?.background?.paper, padding: 1 }}>
        <Grid display="flex" justifyContent="center" alignItems="center" size="grow">
          <Swiper
            modules={[Virtual]}
            centeredSlides={true}
            centeredSlidesBounds={true}
            slidesPerView={3}
            spaceBetween={0}
            breakpoints={{
              340: {
                slidesPerView: 7,
              },
              600: {
                slidesPerView: 11,
              },
              900: {
                slidesPerView: 15,
              },
              1200: {
                slidesPerView: 19,
              },
            }}
            virtual
            initialSlide={daysFromCenterToVisibleEdge}
            onSwiper={(swiper) => (swiperRef.current = swiper)}
            onSlideChange={(swiper) => {
              const index = swiper.activeIndex;
              setCenteredDaysFromStart(visibleDaysFromStart[index]);
            }}
            onReachEnd={() => {
              setDaysFromStartToVisibleEnd((prev) => prev + daysFromCenterToVisibleEdge);
            }}
            onReachBeginning={() => {
              onReachBeginning();
            }}
          >
            {visibleDaysFromStart.map((d, i) => {
              return (
                <SwiperSlide key={i} virtualIndex={i} onClick={() => dateChange(d)} className="center-items">
                  <Avatar
                    sx={{
                      backgroundColor: palette?.background.paper,
                      borderColor: d === selectedDaysFromStart ? palette?.primary.main : palette?.text.primary,
                      borderWidth: d === selectedDaysFromStart ? 4 : 1,
                      color: d === selectedDaysFromStart ? palette?.primary.main : palette?.text.primary,
                      display: "grid",
                      placeItems: "center",
                    }}
                    variant="rounded"
                  >
                    <div style={{ fontSize: "1.5rem" }}>{startDate.getAddedDate(d)}</div>
                    <div
                      style={{
                        fontSize: "0.5rem",
                        color:
                          d === selectedDaysFromStart
                            ? palette?.primary.main
                            : startDate.getAddedDay(d) === Day.Sun
                              ? "red"
                              : startDate.getAddedDay(d) === Day.Sat
                                ? "skyblue"
                                : palette?.text?.primary,
                      }}
                    >
                      {startDate.getAddedDay(d)}
                    </div>
                  </Avatar>
                </SwiperSlide>
              );
            })}
          </Swiper>
        </Grid>
      </Grid>
    </>
  );
}
