import "./style.css";
import { VueFlow, useVueFlow } from "@vue-flow/core";

export default {
  components: {
    VueFlow,
  },
  setup() {
    return {
      ...useVueFlow(),
    };
  },
  template: `
    <vue-flow elevate-edges-on-select="true" fit-view-on-init="true">
      <!-- Forward all slots for custom nodes -->
      <template v-for="(_, slotName) in $slots" v-slot:[slotName]="slotProps">
        <slot :name="slotName" v-bind="slotProps ?? {}" />
      </template>
    </vue-flow>
  `,
};
