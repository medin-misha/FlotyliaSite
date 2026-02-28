import StringComp from '@/components/subComponents/fieldsComps/stringComp.vue'
import NumberComp from '@/components/subComponents/fieldsComps/numberComp.vue'
import StringCreateComp from '@/components/subComponents/createComps/stringCreateComp.vue'
import SelectComp from '@/components/subComponents/fieldsComps/selectComp.vue'
import NumberCreateComp from '@/components/subComponents/createComps/numberCreateComp.vue'
import SelectCreateComp from '@/components/subComponents/createComps/selectCreateComp.vue'

export const productSchema = {
  endpoint: '/product',
  filters: [
    {
      key: 'status',
    },
    {
      key: 'type',
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
      key: 'price',
      label: 'Price',
      type: 'number',
      component: NumberComp,
    },
    {
      key: 'quantity',
      label: 'Quantity',
      type: 'number',
      component: NumberComp,
    },
    {
      key: 'description',
      label: 'Description',
      type: 'string',
      component: StringComp,
    },
    {
      key: 'contract_id',
      label: 'Contract ID',
      type: 'number',
      component: NumberComp,
    },
    {
      key: 'type',
      label: 'Type',
      type: 'string',
      component: SelectComp,
      options: [
        { value: 'damage', label: 'Damage' },
        { value: 'theft', label: 'Theft' },
        { value: 'other', label: 'Other' },
      ],
    },
    {
      key: 'status',
      label: 'Status',
      type: 'string',
      component: SelectComp,
      options: [
        { value: 'open', label: 'Open' },
        { value: 'closed', label: 'Closed' },
        { value: 'resolved', label: 'Resolved' },
        { value: 'in_progress', label: 'In Progress' },
      ],
    },
  ],
}

export const productCreateSchema = {
  endpoint: '/product',
  fields: [
    {
      key: 'name',
      label: 'Name',
      type: 'string',
      component: StringCreateComp,
    },
    {
      key: 'price',
      label: 'Price',
      type: 'number',
      component: NumberCreateComp,
    },
    {
      key: 'quantity',
      label: 'Quantity',
      type: 'number',
      component: NumberCreateComp,
    },
    {
      key: 'description',
      label: 'Description',
      type: 'string',
      component: StringCreateComp,
    },
    {
      key: 'contract_id',
      label: 'Contract ID',
      type: 'number',
      component: NumberCreateComp,
    },
    {
      key: 'type',
      label: 'Type',
      type: 'string',
      component: SelectCreateComp,
      options: [
        { value: 'damage', label: 'Damage' },
        { value: 'theft', label: 'Theft' },
        { value: 'other', label: 'Other' },
      ],
    },
    {
      key: 'status',
      label: 'Status',
      type: 'string',
      component: SelectCreateComp,
      options: [
        { value: 'open', label: 'Open' },
        { value: 'closed', label: 'Closed' },
        { value: 'resolved', label: 'Resolved' },
        { value: 'in_progress', label: 'In Progress' },
      ],
    },
  ],
}
