import { NBA_ORVERTIME_SECONDS, NBA_REGULATION_PERIOD_SECONDS } from "../conf";
import { Periods } from "../types/gameDetail";

function createRegulationGameClock(
  elapsedMs: number,
  regulationSeconds: number = NBA_REGULATION_PERIOD_SECONDS,
): { regulation: number; minutes: string; seconds: string; string: string } {
  const ms = regulationSeconds * 4 * 1000 - elapsedMs;
  const minutes = Math.floor(
    ms == regulationSeconds * 4 * 1000 ? regulationSeconds / 60 : (ms % (regulationSeconds * 1000)) / (60 * 1000),
  )
    .toString()
    .padStart(2, "0");
  const seconds = ((ms % 60000) / 1000).toString().padStart(2, "0");
  const quarter =
    ms < regulationSeconds * 1000
      ? 4
      : ms < regulationSeconds * 2 * 1000
        ? 3
        : ms < regulationSeconds * 3 * 1000
          ? 2
          : 1;
  return {
    regulation: quarter,
    minutes,
    seconds,
    string: `${quarter}Q ${minutes}:${seconds}`,
  };
}

function createOverTimeGameClock(
  elapsedMs: number,
  overTimeSeconds: number = NBA_ORVERTIME_SECONDS,
  regulationSeconds: number = NBA_REGULATION_PERIOD_SECONDS,
): { overTime: number; minutes: string; seconds: string; string: string } {
  const elapsedMsInOverTime = elapsedMs - regulationSeconds * 4 * 1000;
  const maxOverTime = Math.floor(elapsedMsInOverTime / (overTimeSeconds * 1000)) + 1;
  const ms = overTimeSeconds * maxOverTime * 1000 - elapsedMsInOverTime;
  const minutes = Math.floor(
    ms == overTimeSeconds * maxOverTime * 1000 ? overTimeSeconds / 60 : (ms % (overTimeSeconds * 1000)) / (60 * 1000),
  )
    .toString()
    .padStart(2, "0");
  const seconds = ((ms % 60000) / 1000).toString().padStart(2, "0");
  let overTime = 1;
  for (let i = 1; i <= maxOverTime; i++) {
    if (elapsedMsInOverTime <= overTimeSeconds * i * 1000) {
      overTime = i;
      break;
    }
  }
  return { overTime, minutes, seconds, string: `${overTime}OT ${minutes}:${seconds}` };
}

/**
 * 試合の経過時間（ミリ秒）をゲームクロックに変換します.
 */
export function convertFromElapsedMsToGameClock(
  elapsedMs: number,
  period: Periods,
  regulationSeconds: number = NBA_REGULATION_PERIOD_SECONDS,
  overTimeSeconds: number = NBA_ORVERTIME_SECONDS,
): { regulation?: number; overTime?: number; minutes: string; seconds: string; string: string } {
  switch (period) {
    case Periods.firstQuarter: {
      const ms = regulationSeconds * 1000 - elapsedMs;
      const minutes = Math.floor(
        ms == regulationSeconds * 1000 ? regulationSeconds / 60 : (ms % (regulationSeconds * 1000)) / (60 * 1000),
      )
        .toString()
        .padStart(2, "0");
      const seconds = ((ms % 60000) / 1000).toString().padStart(2, "0");
      return {
        regulation: 1,
        minutes,
        seconds,
        string: `1Q ${minutes}:${seconds}`,
      };
    }
    case Periods.secondQuarter: {
      const ms = regulationSeconds * 2 * 1000 - elapsedMs;
      const minutes = Math.floor(
        ms == regulationSeconds * 1000 ? regulationSeconds / 60 : (ms % (regulationSeconds * 1000)) / (60 * 1000),
      )
        .toString()
        .padStart(2, "0");
      const seconds = ((ms % 60000) / 1000).toString().padStart(2, "0");
      return {
        regulation: 2,
        minutes,
        seconds,
        string: `2Q ${minutes}:${seconds}`,
      };
    }
    case Periods.firstHalf: {
      const ms = regulationSeconds * 2 * 1000 - elapsedMs;
      const minutes = Math.floor(
        ms == regulationSeconds * 2 * 1000 ? regulationSeconds / 60 : (ms % (regulationSeconds * 1000)) / (60 * 1000),
      )
        .toString()
        .padStart(2, "0");
      const seconds = ((ms % 60000) / 1000).toString().padStart(2, "0");
      const quarter = ms < regulationSeconds * 1000 ? 2 : 1;
      return {
        regulation: quarter,
        minutes,
        seconds,
        string: `${quarter}Q ${minutes}:${seconds}`,
      };
    }
    case Periods.thirdQuarter: {
      const ms = regulationSeconds * 3 * 1000 - elapsedMs;
      const minutes = Math.floor(
        ms == regulationSeconds * 1000 ? regulationSeconds / 60 : (ms % (regulationSeconds * 1000)) / (60 * 1000),
      )
        .toString()
        .padStart(2, "0");
      const seconds = ((ms % 60000) / 1000).toString().padStart(2, "0");
      return {
        regulation: 3,
        minutes,
        seconds,
        string: `3Q ${minutes}:${seconds}`,
      };
    }
    case Periods.fourthQuarter: {
      const ms = regulationSeconds * 4 * 1000 - elapsedMs;
      const minutes = Math.floor(
        ms == regulationSeconds * 1000 ? regulationSeconds / 60 : (ms % (regulationSeconds * 1000)) / (60 * 1000),
      )
        .toString()
        .padStart(2, "0");
      const seconds = ((ms % 60000) / 1000).toString().padStart(2, "0");
      return {
        regulation: 4,
        minutes,
        seconds,
        string: `4Q ${minutes}:${seconds}`,
      };
    }
    case Periods.secondHalf: {
      const ms = regulationSeconds * 4 * 1000 - elapsedMs;
      const minutes = Math.floor(
        ms == regulationSeconds * 2 * 1000 ? regulationSeconds / 60 : (ms % (regulationSeconds * 1000)) / (60 * 1000),
      )
        .toString()
        .padStart(2, "0");
      const seconds = ((ms % 60000) / 1000).toString().padStart(2, "0");
      const quarter = ms < regulationSeconds * 1000 ? 4 : 3;
      return {
        regulation: quarter,
        minutes,
        seconds,
        string: `${quarter}Q ${minutes}:${seconds}`,
      };
    }
    case Periods.regulation:
      return createRegulationGameClock(elapsedMs);
    case Periods.overTime:
      return createOverTimeGameClock(elapsedMs, overTimeSeconds);
    case Periods.all: {
      if (elapsedMs <= regulationSeconds * 4 * 1000) {
        return createRegulationGameClock(elapsedMs);
      } else {
        return createOverTimeGameClock(elapsedMs, overTimeSeconds);
      }
    }
  }
}

function isPeriod(value: string): value is Periods {
  return (Object.values(Periods) as readonly string[]).includes(value);
}

/**
 * 任意の文字列を Periods 型に変換します.
 */
export function toPeriod(value: string): Periods {
  if (!isPeriod(value)) {
    throw new Error(`Invalid period: ${value}`);
  }
  return value;
}
