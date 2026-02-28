import { defineStore } from 'pinia'

class State {
  constructor(msg, state) {
    this.state = state
    this.msg = msg
  }
}

export const useRequestStates = defineStore('requestStates', {
  state: () => ({
    states: {
      waiting: new State('ЖдЭмс...', 'WAITING'),
      networkError: new State(
        'Не получаеться связаться с сервером\nили на сервере произошка ошибка(((',
        'Network Error',
      ),
      emptyList: new State('Тут пусто((((', 'EmptyList'),
    },
    state: new State('ЖдЭмс...', 'WAITING'),
  }),
  actions: {
    setState(key) {
      this.state = this.states[key]
    },
  },
})
