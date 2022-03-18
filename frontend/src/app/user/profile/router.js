const Module = () => import("./Module.vue");
const Home = () => import("./views/Home.vue");

const routes = [
  {
    path: "profile",
    component: Module,
    children: [
      {
        path: "/",
        component: Home,
      },
    ],
  },
];

export default routes;
