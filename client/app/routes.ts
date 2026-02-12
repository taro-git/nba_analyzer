import { index, route, type RouteConfig } from "@react-router/dev/routes";

export const BASE_URL = "view";

/*
 * ルート定義
 */
export default [
  route(BASE_URL, "routes/layout.tsx", [
    index("routes/home.tsx"),
    route("teams", "routes/teams.tsx"),
    route("players", "routes/players.tsx"),
    route("games", "routes/games.tsx"),
    route("analysis", "routes/analysis.tsx"),
    route("settings", "routes/settings.tsx"),
  ]),
] satisfies RouteConfig;
