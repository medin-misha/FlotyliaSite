import StringComp from '@/components/subComponents/fieldsComps/stringComp.vue'
import NumberComp from '@/components/subComponents/fieldsComps/numberComp.vue'
import stringCreateComp from '@/components/subComponents/createComps/stringCreateComp.vue'

export const adminSchema = {
  endpoint: '/admin',
  fields: [
    {
      key: 'id',
      label: 'ID',
      type: 'number',
      component: NumberComp,
      readonly: true,
    },

    {
      key: 'username',
      label: 'Username',
      type: 'string',
      readonly: true,
      component: StringComp,
    },

    {
      key: 'hashed_password',
      label: 'Password',
      type: 'string',
      inputType: 'password',
      readonly: true,
      component: StringComp,
    },

    {
      key: 'last_login_at',
      label: 'Last login',
      type: 'datetime',
      readonly: true,
      component: StringComp,
    },

    {
      key: 'created_at',
      label: 'Created at',
      type: 'datetime',
      readonly: true,
      component: StringComp,
    },
  ],
}
export const adminCreateSchema = {
  endpoint: '/admin',
  fields: [
    {
      key: 'username',
      label: 'Username',
      type: 'string',
      component: stringCreateComp,
    },

    {
      key: 'password',
      label: 'Password',
      type: 'string',
      inputType: 'password',
      component: stringCreateComp,
    },
  ],
}
