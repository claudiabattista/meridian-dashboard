<template>
  <div class="restock">
    <div class="page-header">
      <h2>{{ t('restock.title') }}</h2>
      <p>{{ t('restock.description') }}</p>
    </div>

    <!-- Budget input -->
    <div class="card budget-card">
      <div class="budget-form">
        <div class="budget-field">
          <label class="budget-label">{{ t('restock.budgetLabel') }}</label>
          <div class="budget-input-wrap">
            <span class="currency-symbol">{{ currencySymbol }}</span>
            <input
              v-model.number="budgetInput"
              type="number"
              min="0"
              step="100"
              :placeholder="t('restock.budgetPlaceholder')"
              class="budget-input"
              @keyup.enter="loadRecommendations"
            />
          </div>
        </div>
        <button class="btn-primary" @click="loadRecommendations" :disabled="loading">
          {{ t('restock.getRecommendations') }}
        </button>
      </div>
    </div>

    <div v-if="loading" class="loading">{{ t('common.loading') }}</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else-if="hasLoaded">

      <!-- Summary bar -->
      <div class="summary-bar" v-if="recommendations.length">
        <div class="summary-item">
          <span class="summary-label">{{ t('restock.totalEstimated') }}</span>
          <span class="summary-value">{{ currencySymbol }}{{ formatNumber(totalCost) }}</span>
        </div>
        <div class="summary-item" v-if="activeBudget > 0">
          <span class="summary-label">{{ t('restock.withinBudget') }}</span>
          <span class="summary-value budget-remaining" :class="{ over: totalCost > activeBudget }">
            {{ currencySymbol }}{{ formatNumber(activeBudget - totalCost) }} remaining
          </span>
        </div>
        <div class="summary-item" v-else>
          <span class="summary-label-dim">{{ t('restock.noBudget') }}</span>
        </div>
        <div class="summary-counts">
          <span class="count-badge critical" v-if="criticalCount">{{ criticalCount }} Critical</span>
          <span class="count-badge urgent" v-if="urgentCount">{{ urgentCount }} Urgent</span>
          <span class="count-badge low" v-if="lowCount">{{ lowCount }} Low</span>
        </div>
      </div>

      <!-- Recommendations table -->
      <div class="card" v-if="recommendations.length">
        <div class="table-container">
          <table>
            <thead>
              <tr>
                <th>{{ t('restock.table.urgency') }}</th>
                <th>{{ t('restock.table.sku') }}</th>
                <th>{{ t('restock.table.name') }}</th>
                <th>{{ t('restock.table.warehouse') }}</th>
                <th>{{ t('restock.table.currentStock') }}</th>
                <th>{{ t('restock.table.daysOfStock') }}</th>
                <th>{{ t('restock.table.forecastedDemand') }}</th>
                <th>{{ t('restock.table.recommendedQty') }}</th>
                <th>{{ t('restock.table.unitCost') }}</th>
                <th>{{ t('restock.table.totalCost') }}</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="rec in recommendations" :key="rec.sku">
                <td>
                  <span :class="['badge', urgencyClass(rec.urgency)]">
                    {{ t(`restock.urgency.${rec.urgency}`) }}
                  </span>
                </td>
                <td><strong>{{ rec.sku }}</strong></td>
                <td>{{ translateProductName(rec.name) }}</td>
                <td>{{ translateWarehouse(rec.warehouse) }}</td>
                <td>{{ rec.current_stock.toLocaleString() }}</td>
                <td>
                  <span :class="['days-pill', urgencyClass(rec.urgency)]">
                    {{ rec.days_of_stock }}d
                  </span>
                </td>
                <td>{{ rec.forecasted_demand.toLocaleString() }} / 30d</td>
                <td><strong>{{ rec.recommended_quantity.toLocaleString() }}</strong></td>
                <td>{{ currencySymbol }}{{ rec.unit_cost.toFixed(2) }}</td>
                <td><strong>{{ currencySymbol }}{{ formatNumber(rec.total_cost) }}</strong></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Empty state -->
      <div class="empty-state" v-else>
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
          <path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <p>{{ t('restock.noResults') }}</p>
      </div>

    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { api } from '../api'
import { useI18n } from '../composables/useI18n'

export default {
  name: 'Restock',
  setup() {
    const { t, currentCurrency, translateProductName, translateWarehouse } = useI18n()

    const currencySymbol = computed(() => currentCurrency.value === 'JPY' ? '¥' : '$')

    const loading = ref(false)
    const error = ref(null)
    const recommendations = ref([])
    const budgetInput = ref(null)
    const activeBudget = ref(0)
    const hasLoaded = ref(false)

    const totalCost = computed(() =>
      recommendations.value.reduce((sum, r) => sum + r.total_cost, 0)
    )

    const criticalCount = computed(() => recommendations.value.filter(r => r.urgency === 'critical').length)
    const urgentCount = computed(() => recommendations.value.filter(r => r.urgency === 'urgent').length)
    const lowCount = computed(() => recommendations.value.filter(r => r.urgency === 'low').length)

    const loadRecommendations = async () => {
      try {
        loading.value = true
        error.value = null
        activeBudget.value = budgetInput.value || 0
        recommendations.value = await api.getRestockRecommendations(budgetInput.value)
        hasLoaded.value = true
      } catch (err) {
        error.value = 'Failed to load recommendations: ' + err.message
      } finally {
        loading.value = false
      }
    }

    const formatNumber = (num) =>
      Number(num).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })

    const urgencyClass = (urgency) => {
      if (urgency === 'critical') return 'danger'
      if (urgency === 'urgent') return 'warning'
      return 'info'
    }

    onMounted(loadRecommendations)

    return {
      t,
      currencySymbol,
      loading,
      error,
      recommendations,
      budgetInput,
      activeBudget,
      hasLoaded,
      totalCost,
      criticalCount,
      urgentCount,
      lowCount,
      loadRecommendations,
      formatNumber,
      urgencyClass,
      translateProductName,
      translateWarehouse
    }
  }
}
</script>

<style scoped>
.restock {
  padding: 0;
}

.budget-card {
  margin-bottom: 1.25rem;
}

.budget-form {
  display: flex;
  align-items: flex-end;
  gap: 1rem;
  flex-wrap: wrap;
}

.budget-field {
  display: flex;
  flex-direction: column;
  gap: 0.375rem;
  flex: 1;
  min-width: 240px;
  max-width: 360px;
}

.budget-label {
  font-size: 0.813rem;
  font-weight: 600;
  color: #475569;
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

.budget-input-wrap {
  position: relative;
  display: flex;
  align-items: center;
}

.currency-symbol {
  position: absolute;
  left: 0.75rem;
  color: #64748b;
  font-size: 0.938rem;
  pointer-events: none;
}

.budget-input {
  width: 100%;
  padding: 0.563rem 0.75rem 0.563rem 1.75rem;
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  font-size: 0.938rem;
  color: #0f172a;
  background: #f8fafc;
  transition: all 0.2s;
}

.budget-input:focus {
  outline: none;
  border-color: #3b82f6;
  background: white;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.budget-input::placeholder {
  color: #94a3b8;
}

.btn-primary {
  padding: 0.563rem 1.25rem;
  background: #2563eb;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 0.938rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
  white-space: nowrap;
}

.btn-primary:hover:not(:disabled) {
  background: #1d4ed8;
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: default;
}

/* Summary bar */
.summary-bar {
  display: flex;
  align-items: center;
  gap: 2rem;
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  padding: 1rem 1.5rem;
  margin-bottom: 1.25rem;
  flex-wrap: wrap;
}

.summary-item {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.summary-label {
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: #64748b;
}

.summary-label-dim {
  font-size: 0.813rem;
  color: #94a3b8;
}

.summary-value {
  font-size: 1.375rem;
  font-weight: 700;
  color: #0f172a;
}

.budget-remaining {
  color: #059669;
}

.budget-remaining.over {
  color: #dc2626;
}

.summary-counts {
  display: flex;
  gap: 0.5rem;
  align-items: center;
  margin-left: auto;
}

.count-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 700;
}

.count-badge.critical {
  background: #fecaca;
  color: #991b1b;
}

.count-badge.urgent {
  background: #fed7aa;
  color: #92400e;
}

.count-badge.low {
  background: #dbeafe;
  color: #1e40af;
}

/* Days pill */
.days-pill {
  display: inline-block;
  padding: 0.2rem 0.6rem;
  border-radius: 9999px;
  font-size: 0.8rem;
  font-weight: 700;
}

.days-pill.danger {
  background: #fecaca;
  color: #991b1b;
}

.days-pill.warning {
  background: #fed7aa;
  color: #92400e;
}

.days-pill.info {
  background: #dbeafe;
  color: #1e40af;
}

/* Empty state */
.empty-state {
  text-align: center;
  padding: 4rem 2rem;
  color: #64748b;
}

.empty-state svg {
  width: 48px;
  height: 48px;
  color: #059669;
  margin: 0 auto 1rem;
  display: block;
}

.empty-state p {
  font-size: 1rem;
}

.loading,
.error {
  padding: 2rem;
  text-align: center;
  color: #64748b;
}

.error {
  color: #ef4444;
}
</style>
