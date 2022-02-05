const Module = () => import("./Module.vue");
const Home = () => import("./views/Home.vue");

const route = {
  path: "/admin",
  component: Module,
  meta: {
    requiresAdmin: true,
  },
  children: [
    {
      path: "/",
      component: Home,
    },
  ],
};

export default [route];
