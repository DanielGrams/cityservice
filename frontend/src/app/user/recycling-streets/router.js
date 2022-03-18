const Module = () => import("./Module.vue");
const PlaceList = () => import("./views/PlaceList.vue");
const RecyclingStreetList = () => import("./views/RecyclingStreetList.vue");

const routes = [
  {
    path: "recycling-streets",
    component: Module,
    children: [
      {
        path: "places",
        component: PlaceList,
      },
      {
        path: "places/:placeId/recycling-streets",
        component: RecyclingStreetList,
      },
    ],
  },
];

export default routes;
