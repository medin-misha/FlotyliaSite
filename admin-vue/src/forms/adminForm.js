import StringComp from '@/components/subComponents/fieldsComps/stringComp.vue'
import NumberComp from '@/components/subComponents/fieldsComps/numberComp.vue'

export const adminSchema = {
  endpoint: '/admin',
  fields: [
    {
      key: 'id',
      label: 'ID',
      type: 'number',
      component: NumberComp,
      readonly: true,
      group: 'system',
    },

    {
      key: 'username',
      label: 'Имя',
      type: 'string',
      readonly: true,
      component: StringComp,
      group: 'personal',
    },

    {
      key: 'hashed_password',
      label: 'Пароль',
      type: 'string',
      inputType: 'password',
      readonly: true,
      component: StringComp,
      group: 'system',
    },

    {
      key: 'last_login_at',
      label: 'Последняя аутентификация',
      type: 'datetime',
      readonly: true,
      component: StringComp,
      group: 'system',
    },

    {
      key: 'created_at',
      label: 'Создан',
      type: 'datetime',
      readonly: true,
      component: StringComp,
      group: 'system',
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
      component: StringComp,
    },

    {
      key: 'password',
      label: 'Пароль',
      type: 'string',
      inputType: 'password',
      component: StringComp,
    },
  ],
}
