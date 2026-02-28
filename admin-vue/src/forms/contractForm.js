import StringComp from '@/components/subComponents/fieldsComps/stringComp.vue'
import NumberComp from '@/components/subComponents/fieldsComps/numberComp.vue'
import FileComp from '@/components/subComponents/fieldsComps/fileComp.vue'
import CheckboxComp from '@/components/subComponents/fieldsComps/checkboxComp.vue'
import StringCreateComp from '@/components/subComponents/createComps/stringCreateComp.vue'
import DateCreateComp from '@/components/subComponents/createComps/dateCreateComp.vue'
import FileCreateComp from '@/components/subComponents/createComps/fileCreateComp.vue'

export const contractSchema = {
  endpoint: '/contracts',
  fields: [
    {
      key: 'id',
      label: 'ID',
      type: 'number',
      readonly: true,
      component: NumberComp,  
    },

    {
      key: 'contract_file',
      label: 'Contract file',
      type: 'number',
      isFile: true,
      component: FileComp,
    },

    {
      key: 'transport_id',
      label: 'Transport',
      type: 'number',
      readonly: false,
      component: NumberComp,
    },

    {
      key: 'user_id',
      label: 'User',
      type: 'number',
      readonly: false,
      component: NumberComp,
    },

    {
      key: 'date_of_signing',
      label: 'Date of signing',
      type: 'datetime',
      component: StringComp,
    },

    {
      key: 'is_active',
      label: 'Active',
      type: 'boolean',
      component: CheckboxComp,
    },
  ],
}

export const contractCreateSchema = {
  endpoint: '/contracts',
  fields: [
    {
      key: 'transport_id',
      label: 'Transport ID',
      type: 'number',
      component: StringCreateComp,
    },
    {
      key: 'user_id',
      label: 'User ID',
      type: 'number',
      component: StringCreateComp,
    },
    {
      key: 'date_of_signing',
      label: 'Date of signing',
      type: 'date',
      component: DateCreateComp,
    },
    {
      key: 'contract_file',
      label: 'Contract file',
      type: 'file',
      component: FileCreateComp,
    },
  ],
}
