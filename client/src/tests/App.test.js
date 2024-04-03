import { mount } from "@vue/test-utils";
import { createPinia, setActivePinia } from "pinia";
import AppComponent from "../App.vue";
import { describe, it, beforeEach } from "vitest";


describe("AppComponent", () => {
  beforeEach(() => {
    setActivePinia(createPinia());
  });

  it('should have a p element with "Group Management Application" text', () => {
    const wrapper = mount(AppComponent);
    wrapper.exists();
  });
});
