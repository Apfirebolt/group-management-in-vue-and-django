import { mount } from '@vue/test-utils';
import ConfirmModal from '../components/ConfirmModal.vue';
import { describe, expect, it } from "vitest";


describe('ConfirmModal', () => {

    const passedProps = {
        message: 'Are you sure you want to delete this group?',
        confirmAction: function() {},
        cancelAction: function() {}
    };

    it('should have a button element with "Cancel" text', () => {
        const wrapper = mount(ConfirmModal, {
            propsData: {
                message: 'Are you sure you want to delete this group?',
                confirmAction: function() {},
                cancelAction: function() {}
            }
        });
        const buttonElement = wrapper.findAll('button').at(0);
        expect(buttonElement.exists()).toBe(true);
        expect(buttonElement.text()).toContain('Cancel');
    });

    // Button of type submit with "Confirm" text
    it('should have a button element with "Confirm" text', () => {
        const wrapper = mount(ConfirmModal, {
            propsData: {
                message: 'Are you sure you want to delete this group?',
                confirmAction: function() {},
                cancelAction: function() {}
            }
        });
        const buttonElement = wrapper.findAll('button').at(1);
        expect(buttonElement.exists()).toBe(true);
        expect(buttonElement.text()).toContain('Confirm');
        expect(buttonElement.attributes().type).toBe('submit'); 
    });
});
