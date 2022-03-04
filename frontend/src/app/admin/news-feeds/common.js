import i18n from "@/i18n";

export function localizeFeedType(value) {
  return i18n.t(`app.admin.newsFeeds.feedTypes.${value}`);
}

export function getLocalizedFeedTypes() {
  const feed_types = [
    "unknown",
    "city",
    "district",
    "police",
    "fire_department",
    "culture",
    "citizen_participation",
    "civil_protection",
  ];

  let localized = feed_types.map(function (t) {
    return {
      value: t,
      text: localizeFeedType(t),
    };
  });

  localized.sort(function (a, b) {
    return a.text > b.text ? 1 : -1;
  });

  return localized;
}
