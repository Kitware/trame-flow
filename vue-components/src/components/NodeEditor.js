import "./style.css";
import { VueFlow, useVueFlow } from "@vue-flow/core";
import { Background } from "@vue-flow/background";
import { MiniMap } from "@vue-flow/minimap";

export default {
  components: {
    VueFlow,
    Background,
    MiniMap,
  },
  props: {
    backgroundPatternVariant: {
      type: "dots" | "lines",
      default: "dots",
    },
    backgroundPatternColor: {
      type: String,
      default: "#81818a",
    },
    backgroundPatternSize: {
      type: Number,
      default: 1,
    },
    backgroundPatternGap: {
      type: Number,
      default: 10,
    },
  },
  setup() {
    return {
      ...useVueFlow(),
    };
  },
  template: `
    <vue-flow>
      <background :variant="backgroundPatternVariant" :pattern-color="backgroundPatternColor" :size="backgroundPatternSize" :gap="backgroundPatternGap" />
      <mini-map />
    </vue-flow>
  `,
};
