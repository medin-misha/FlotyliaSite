// Маркёр-схема для пункта меню «Статистика».
// Не имеет полей: рендерится отдельным компонентом receiptStatsComp через view: 'stats'.
export const receiptStatsSchema = {
  endpoint: '/receipts',
  name: 'Статистика',
  view: 'stats',
}
