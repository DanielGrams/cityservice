const Module = () => import("./Module.vue");
const Login = () => import("./views/Login.vue");

const routes = [
  {
    path: "/",
    component: Module,
    meta: {
      requiresAnonymous: true,
    },
    children: [
      {
        path: "/login",
        component: Login,
      },
    ],
  },
];

export default routes;
