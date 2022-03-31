const Module = () => import("./Module.vue");
const LegalNotice = () => import("./views/LegalNotice.vue");
const Privacy = () => import("./views/Privacy.vue");

const routes = [
  {
    path: "/",
    component: Module,
    children: [
      {
        path: "/impressum",
        component: LegalNotice,
      },
      {
        path: "/datenschutz",
        component: Privacy,
      },
    ],
  },
];

export default routes;
