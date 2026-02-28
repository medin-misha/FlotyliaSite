import StringComp from '@/components/subComponents/fieldsComps/stringComp.vue'
import NumberComp from '@/components/subComponents/fieldsComps/numberComp.vue'
import StringCreateComp from '@/components/subComponents/createComps/stringCreateComp.vue'
import NumberCreateComp from '@/components/subComponents/createComps/numberCreateComp.vue'

export const transportSchema = {
  endpoint: '/transports',
  fields: [
    {
      key: 'id',
      label: 'ID',
      type: 'number',
      readonly: true,
      component: NumberComp,
    },

    {
      key: 'type',
      label: 'Type',
      type: 'string',
      component: StringComp,
    },

    {
      key: 'manufacturer',
      label: 'Manufacturer',
      type: 'string',
      component: StringComp,
    },

    {
      key: 'model',
      label: 'Model',
      type: 'string',
      component: StringComp,
    },

    {
      key: 'color',
      label: 'Color',
      type: 'string',
      component: StringComp,
    },

    {
      key: 'number',
      label: 'Number',
      type: 'string',
      component: StringComp,
    },
    {
      key: 'message',
      label: 'Message',
      type: 'string',
      component: StringComp,
    },
    {
      key: 'rental_price',
      label: 'Rental Price',
      type: 'number',
      component: NumberComp,
    },
  ],
}

export const transportCreateSchema = {
  endpoint: '/transports',
  fields: [
    {
      key: 'type',
      label: 'Type',
      type: 'string',
      component: StringCreateComp,
    },
    {
      key: 'manufacturer',
      label: 'Manufacturer',
      type: 'string',
      component: StringCreateComp,
    },
    {
      key: 'model',
      label: 'Model',
      type: 'string',
      component: StringCreateComp,
    },
    {
      key: 'color',
      label: 'Color',
      type: 'string',
      component: StringCreateComp,
    },
    {
      key: 'number',
      label: 'Number',
      type: 'string',
      component: StringCreateComp,
    },
    {
      key: 'message',
      label: 'Message',
      type: 'string',
      component: StringCreateComp,
    },
    {
      key: 'rental_price',
      label: 'Rental Price',
      type: 'number',
      component: NumberCreateComp,
    },
  ],
}
