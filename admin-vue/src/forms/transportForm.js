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
      label: 'Тип',
      type: 'string',
      component: StringComp,
    },

    {
      key: 'manufacturer',
      label: 'Производитель',
      type: 'string',
      component: StringComp,
    },

    {
      key: 'model',
      label: 'Модель',
      type: 'string',
      component: StringComp,
    },

    {
      key: 'color',
      label: 'Цвет',
      type: 'string',
      component: StringComp,
    },

    {
      key: 'number',
      label: 'Номер',
      type: 'string',
      component: StringComp,
    },
    {
      key: 'message',
      label: 'Сообщение',
      type: 'string',
      component: StringComp,
    },
    {
      key: 'rental_price',
      label: 'Цена аренды',
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
      label: 'Тип',
      type: 'string',
      component: StringCreateComp,
    },
    {
      key: 'manufacturer',
      label: 'Производитель',
      type: 'string',
      component: StringCreateComp,
    },
    {
      key: 'model',
      label: 'Модель',
      type: 'string',
      component: StringCreateComp,
    },
    {
      key: 'color',
      label: 'Цвет',
      type: 'string',
      component: StringCreateComp,
    },
    {
      key: 'number',
      label: 'Номер',
      type: 'string',
      component: StringCreateComp,
    },
    {
      key: 'message',
      label: 'Сообщение',
      type: 'string',
      component: StringCreateComp,
    },
    {
      key: 'rental_price',
      label: 'Цена аренды',
      type: 'number',
      component: NumberCreateComp,
    },
  ],
}
