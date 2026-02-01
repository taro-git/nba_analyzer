import { index, prefix, route, type RouteConfig } from "@react-router/dev/routes";

export default [
  ...prefix("view", [
    index("routes/home.tsx"),
    route("seasons", "routes/seasons.tsx"),
    route("games", "routes/games.tsx"),
    route("analysis", "routes/analysis.tsx"),
  ]),
] satisfies RouteConfig;
