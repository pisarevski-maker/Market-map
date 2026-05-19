// Czech Steel Dashboard — Map Settings
const MAP_SETTINGS = {
  // Czechia bounding box
  bounds: {
    north: 51.06,
    south: 48.55,
    west:  12.09,
    east:  18.87,
  },
  center: { lat: 49.75, lon: 15.50 },
  defaultZoom: 7,

  // Marker settings
  markerRadius:       10,
  markerHoverRadius:  13,
  markerColor:        '#9B1C31',
  markerHoverColor:   '#7A1F2B',
  markerStroke:       '#FFFFFF',
  markerStrokeWidth:  2,

  // Tooltip
  tooltipOffset:      { x: 15, y: -10 },

  // Interaction
  hoverDelay:         100,   // ms
  clickAction:        'open_plant_detail',
};

export default MAP_SETTINGS;
