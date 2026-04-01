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
      label: 'Имя ',
      type: 'string',
      readonly: true,
      component: StringComp,
    },

    {
      key: 'hashed_password',
      label: 'Пароль',
      type: 'string',
      inputType: 'password',
      readonly: true,
      component: StringComp,
    },

    {
      key: 'last_login_at',
      label: 'Последнияя аутентификация',
      type: 'datetime',
      readonly: true,
      component: StringComp,
    },

    {
      key: 'created_at',
      label: 'Создан',
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
      label: 'Имя',
      type: 'string',
      component: stringCreateComp,
    },

    {
      key: 'password',
      label: 'Пароль',
      type: 'string',
      inputType: 'password',
      component: stringCreateComp,
    },
  ],
}
