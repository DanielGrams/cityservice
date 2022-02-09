const Module = () => import("./Module.vue");
const List = () => import("./views/List.vue");
const Read = () => import("./views/Read.vue");

const routes = [
  {
    path: "news-feeds",
    component: Module,
    children: [
      {
        path: "/",
        component: List,
      },
      {
        path: ":id",
        component: Read,
      },
    ],
  },
];

export default routes;
