import StringComp from '@/components/subComponents/fieldsComps/stringComp.vue'
import NumberComp from '@/components/subComponents/fieldsComps/numberComp.vue'
import DocumentListComp from '@/components/subComponents/fieldsComps/documentListComp.vue'
import SelectComp from '@/components/subComponents/fieldsComps/selectComp.vue'
import DateComp from '@/components/subComponents/fieldsComps/dateComp.vue'
import stringCreateComp from '@/components/subComponents/createComps/stringCreateComp.vue'
import SelectCreateComp from '@/components/subComponents/createComps/selectCreateComp.vue'
import DateCreateComp from '@/components/subComponents/createComps/dateCreateComp.vue'
export const userSchema = {
  endpoint: '/users',
  filters: [
    {
      key: 'status',
    },
  ],
  fields: [
    {
      key: 'id',
      label: 'ID',
      type: 'number',
      readonly: true,
      component: NumberComp,
    },

    {
      key: 'name',
      label: 'Name',
      type: 'string',
      component: StringComp,
    },

    {
      key: 'email',
      label: 'Email',
      type: 'string',
      component: StringComp,
    },

    {
      key: 'phone',
      label: 'Phone',
      type: 'string',
      component: StringComp,
    },

    {
      key: 'work_in',
      label: 'Work in',
      type: 'string',
      component: StringComp,
    },

    {
      key: 'how_found_it',
      label: 'How found it',
      type: 'string',
      component: StringComp,
    },
    {
      key: 'desired_transport',
      label: 'Desired transport',
      type: 'string',
      component: StringComp,
    },
    {
      key: 'birth_date',
      label: 'Birth date',
      type: 'date',
      component: DateComp,
    },

    {
      key: 'invoice',
      label: 'Invoice',
      type: 'string',
      component: StringComp,
    },

    {
      key: 'status',
      label: 'Status',
      type: 'string',
      readonly: false,
      component: SelectComp,
      options: [
        { value: 'pending', label: 'Pending' },
        { value: 'active', label: 'Active' },
        { value: 'inoperative', label: 'Inoperative' },
      ],
    },

    {
      key: 'telegram',
      label: 'Telegram',
      type: 'string',
      component: StringComp,
    },
    {
      key: 'whatsapp',
      label: 'Whatsapp',
      type: 'string',
      component: StringComp,
    },
    {
      key: 'city',
      label: 'City',
      type: 'string',
      component: StringComp,
    },

    {
      key: 'address',
      label: 'Address',
      type: 'string',
      component: StringComp,
    },

    {
      key: 'stay_type',
      label: 'Stay type',
      type: 'string',
      component: StringComp,
    },
    {
      key: 'documents',
      label: 'Documents',
      type: 'object',
      component: DocumentListComp,
    },
  ],
}

export const userCreateSchema = {
  endpoint: '/users',
  fields: [
    {
      key: 'name',
      label: 'Name',
      type: 'string',
      component: stringCreateComp,
    },

    {
      key: 'email',
      label: 'Email',
      type: 'string',
      component: stringCreateComp,
    },

    {
      key: 'phone',
      label: 'Phone',
      type: 'string',
      component: stringCreateComp,
    },

    {
      key: 'work_in',
      label: 'Work in',
      type: 'string',
      component: stringCreateComp,
    },

    {
      key: 'how_found_it',
      label: 'How found it',
      type: 'string',
      component: stringCreateComp,
    },
    {
      key: 'desired_transport',
      label: 'Desired transport',
      type: 'string',
      component: stringCreateComp,
    },
    {
      key: 'birth_date',
      label: 'Birth date',
      type: 'date',
      component: DateCreateComp,
    },

    {
      key: 'invoice',
      label: 'Invoice',
      type: 'string',
      component: stringCreateComp,
    },

    {
      key: 'status',
      label: 'Status',
      type: 'string',
      readonly: false,
      component: SelectCreateComp,
      options: [
        { value: 'pending', label: 'Pending' },
        { value: 'active', label: 'Active' },
        { value: 'inoperative', label: 'Inoperative' },
      ],
    },

    {
      key: 'telegram',
      label: 'Telegram',
      type: 'string',
      component: stringCreateComp,
    },
    {
      key: 'whatsapp',
      label: 'Whatsapp',
      type: 'string',
      component: stringCreateComp,
    },
    {
      key: 'city',
      label: 'City',
      type: 'string',
      component: stringCreateComp,
    },

    {
      key: 'address',
      label: 'Address',
      type: 'string',
      component: stringCreateComp,
    },

    {
      key: 'stay_type',
      label: 'Stay type',
      type: 'string',
      component: stringCreateComp,
    },
  ],
}
