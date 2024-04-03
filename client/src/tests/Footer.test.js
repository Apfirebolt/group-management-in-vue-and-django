import { mount } from '@vue/test-utils';
import FooterComponent from '../components/FooterComponent.vue';
import { describe, expect, test, it } from "vitest";


describe('FooterComponent', () => {

    it('should have a p element with "Group Management Application" text', () => {
        const wrapper = mount(FooterComponent);
        const pElement = wrapper.find('p');
        expect(pElement.exists()).toBe(true);
        expect(pElement.text()).toContain('2024 Group Management Application');
    });
});
