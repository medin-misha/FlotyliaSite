import StringComp from '@/components/subComponents/fieldsComps/stringComp.vue'
import NumberComp from '@/components/subComponents/fieldsComps/numberComp.vue'
import DateComp from '@/components/subComponents/fieldsComps/dateComp.vue'
import FileComp from '@/components/subComponents/fieldsComps/fileComp.vue'

export const receiptSchema = {
  endpoint: '/receipts',
  fields: [
    {
      key: 'id',
      label: 'ID',
      type: 'number',
      readonly: true,
      component: NumberComp,
      group: 'personal',
    },
    {
      key: 'receipt_date',
      label: 'Дата чека',
      type: 'date',
      copyable: true,
      component: DateComp,
      group: 'personal',
    },
    {
      key: 'amount',
      label: 'Сумма (CZK)',
      type: 'number',
      step: 'any',
      copyable: true,
      component: NumberComp,
      group: 'personal',
    },
    {
      key: 'description',
      label: 'Описание',
      type: 'string',
      copyable: true,
      component: StringComp,
      group: 'personal',
    },
    {
      key: 'created_date',
      label: 'Дата создания',
      type: 'date',
      readonly: true,
      component: DateComp,
      group: 'personal',
    },
    {
      key: 'file_id',
      label: 'Файл чека',
      type: 'number',
      component: FileComp,
      group: 'personal',
    },
  ],
}

export const receiptCreateSchema = {
  endpoint: '/receipts',
  fields: [
    {
      key: 'receipt_date',
      label: 'Дата чека',
      type: 'date',
      required: true,
      component: DateComp,
    },
    {
      key: 'amount',
      label: 'Сумма (CZK)',
      type: 'number',
      step: 'any',
      required: true,
      component: NumberComp,
    },
    {
      key: 'description',
      label: 'Описание',
      type: 'string',
      component: StringComp,
    },
    {
      key: 'file_id',
      label: 'Файл чека',
      type: 'number',
      required: true,
      component: FileComp,
    },
  ],
}
