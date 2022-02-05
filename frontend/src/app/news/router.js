const Module = () => import("./Module.vue");
const Home = () => import("./views/Home.vue");

const route = {
  path: "/news",
  component: Module,
  children: [
    {
      path: "/",
      component: Home,
    },
  ],
};

export default [route];
