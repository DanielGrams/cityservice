const Module = () => import("./Module.vue");
const Profile = () => import("./views/Profile.vue");

const routes = [
  {
    path: "/user",
    component: Module,
    meta: {
      requiresAuth: true,
    },
    children: [
      {
        path: "profile",
        component: Profile,
      },
    ],
  },
];

export default routes;
