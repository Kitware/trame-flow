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
    <vue-flow elevate-edges-on-select="true">
      <background :variant="backgroundPatternVariant" :pattern-color="backgroundPatternColor" :size="backgroundPatternSize" :gap="backgroundPatternGap" />

      <template #node-text="nodeProps">
        {{nodeProps.data.label}}
      </template>

      <mini-map />
    </vue-flow>
  `,
};
