import { shallowMount } from '@vue/test-utils';
import FooterComponent from '../components/FooterComponent.vue';
import { describe, expect, test, it } from "vitest";


describe('FooterComponent', () => {
    it('should load HeaderComponent', () => {
        const wrapper = shallowMount(FooterComponent);
        expect(wrapper.exists()).toBe(true);
    });
});
