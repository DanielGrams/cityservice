const Module = () => import("./Module.vue");
const List = () => import("./views/List.vue");
const Read = () => import("./views/Read.vue");
const NewsList = () => import("./components/NewsList.vue");
const RecyclingStreetList = () => import("./components/RecyclingStreetList.vue");
const WeatherWarningList = () => import("./components/WeatherWarningList.vue");


const routes = [
  {
    path: "/places",
    component: Module,
    children: [
      {
        path: "/",
        component: List,
      },
      {
        path: ":id",
        component: Read,
        children: [
          { path: '', component: NewsList },
          { path: 'recycling', component: RecyclingStreetList },
          { path: 'weather', component: WeatherWarningList },
        ]
      },
    ],
  },
];

export default routes;
