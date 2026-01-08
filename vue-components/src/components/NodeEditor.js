import "./style.css";
import { VueFlow, useVueFlow } from "@vue-flow/core";
import { Background } from "@vue-flow/background";
import { MiniMap } from "@vue-flow/minimap";
import { Controls } from "@vue-flow/controls";

export default {
  components: {
    VueFlow,
    Background,
    MiniMap,
    Controls,
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
    showControls: {
      type: Boolean,
      default: true,
    },
    showMiniMap: {
      type: Boolean,
      default: true,
    },
  },
  setup() {
    return {
      ...useVueFlow(),
    };
  },
  template: `
    <vue-flow elevate-edges-on-select="true" fit-view-on-init="true">
      <background :variant="backgroundPatternVariant" :pattern-color="backgroundPatternColor" :size="backgroundPatternSize" :gap="backgroundPatternGap" />

      <template #node-text="nodeProps">
        {{nodeProps.data.label}}
      </template>

      <controls v-if="showControls" />
      <mini-map v-if="showMiniMap" />
    </vue-flow>
  `,
};
