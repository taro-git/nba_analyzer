import { Welcome } from "../components/welcome/welcome";
import type { Route } from "./+types/home";

export function meta(dummy: Route.MetaArgs) {
  console.log(dummy);
  return [
    {
      title: "New React Router App",
    },
    {
      name: "description",
      content: "Welcome to React Router!",
    },
  ];
}

export default function Home() {
  return <Welcome />;
}
