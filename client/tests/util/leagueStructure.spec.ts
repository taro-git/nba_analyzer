import { describe, expect, it } from "vitest";

import { Conferences, Divisions } from "../../app/types/leagueStructure";
import { ConferenceFromDivisions } from "../../app/util/leagueStructure";

describe("ConferenceFromDivisions (exhaustive)", () => {
  it("maps all divisions correctly", () => {
    const cases: Record<string, string> = {
      [Divisions.Atlantic]: Conferences.East,
      [Divisions.Central]: Conferences.East,
      [Divisions.SouthEast]: Conferences.East,
      [Divisions.NorthWest]: Conferences.West,
      [Divisions.Pacific]: Conferences.West,
      [Divisions.SouthWest]: Conferences.West,
    };

    for (const division of Object.values(Divisions)) {
      expect(ConferenceFromDivisions(division)).toBe(cases[division]);
    }
  });
});
