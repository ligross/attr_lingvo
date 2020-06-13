<template>
    <div class="content">
        <md-toolbar class="md-transparent">
            <div class="md-toolbar-row">
                <h3 class="md-title">Тут какое-то название или описание</h3>
            </div>
        </md-toolbar>

        <md-steppers :md-active-step.sync="active" md-linear>
            <md-step id="first_step" md-label="Первый текст" md-description="Обязательный шаг"
                     :md-done.sync="first_step">
                <md-field md-clearable>
                    <label>Введите первый текст</label>
                    <md-textarea v-model="first_text"></md-textarea>
                </md-field>
                <md-button class="md-raised md-primary" :disabled="!first_text"
                           @click="setDone('first_step', 'second_step')">Продолжить
                </md-button>
            </md-step>

            <md-step id="second_step" md-label="Второй текст" md-description="Обязательный шаг"
                     :md-done.sync="second_step">
                <md-field md-clearable>
                    <label>Введите второй текст</label>
                    <md-textarea v-model="second_text"></md-textarea>
                </md-field>
                <md-button class="md-raised md-primary" :disabled="!second_text"
                           @click="setDone('second_step', 'third_step')">Продолжить
                </md-button>
            </md-step>

            <md-step id="third_step" md-label="Выбор атрибутов" md-description="Опциональный шаг"
                     :md-done.sync="third_step">
                <md-list>
                    <md-subheader>Выберите атрибуты</md-subheader>
                    <md-list-item :key="attributes.flesch_kincaid_index.name">
                        <md-checkbox v-model="attributes.flesch_kincaid_index.checked"/>
                        <span class="md-list-item-text">{{ attributes.flesch_kincaid_index.name }}</span>
                    </md-list-item>
                    <md-list-item :key="attributes.fog_index.name">
                        <md-checkbox v-model="attributes.fog_index.checked"/>
                        <span class="md-list-item-text">{{ attributes.fog_index.name }}</span>
                    </md-list-item>
                    <md-list-item :key="attributes.avg_word_len.name">
                        <md-checkbox v-model="attributes.avg_word_len.checked"/>
                        <span class="md-list-item-text">{{ attributes.avg_word_len.name }}</span>
                    </md-list-item>
                    <md-list-item :key="attributes.avg_sentence_len.name">
                        <md-checkbox v-model="attributes.avg_sentence_len.checked"/>
                        <span class="md-list-item-text">{{ attributes.avg_sentence_len.name }}</span>
                    </md-list-item>
                    <md-list-item :key="attributes.sentence_len8_count.name">
                        <md-checkbox v-model="attributes.sentence_len8_count.checked"/>
                        <span class="md-list-item-text">{{ attributes.sentence_len8_count.name }}</span>
                    </md-list-item>
                    <md-list-item :key="attributes.pr_coefficient.name">
                        <md-checkbox v-model="attributes.pr_coefficient.checked"/>
                        <span class="md-list-item-text">{{ attributes.pr_coefficient.name }}</span>
                    </md-list-item>
                    <md-list-item :key="attributes.qu_coefficient.name">
                        <md-checkbox v-model="attributes.qu_coefficient.checked"/>
                        <span class="md-list-item-text">{{ attributes.qu_coefficient.name }}</span>
                    </md-list-item>
                    <md-list-item :key="attributes.ac_coefficient.name">
                        <md-checkbox v-model="attributes.ac_coefficient.checked"/>
                        <span class="md-list-item-text">{{ attributes.ac_coefficient.name }}</span>
                    </md-list-item>
                    <md-list-item :key="attributes.din_coefficient.name">
                        <md-checkbox v-model="attributes.din_coefficient.checked"/>
                        <span class="md-list-item-text">{{ attributes.din_coefficient.name }}</span>
                    </md-list-item>
                    <md-list-item :key="attributes.con_coefficient.name">
                        <md-checkbox v-model="attributes.con_coefficient.checked"/>
                        <span class="md-list-item-text">{{ attributes.con_coefficient.name }}</span>
                    </md-list-item>
                </md-list>
                <md-button class="md-raised md-primary" @click="setDone('third_step', 'results_step')">Продолжить
                </md-button>
            </md-step>
            <md-step id="results_step" md-label="Результаты" md-description="Просмотр результатов"
                     :md-done.sync="results_step">

                <md-progress-spinner v-if="results.attributes.length === 0" :md-diameter="100" :md-stroke="10"
                                     md-mode="indeterminate"></md-progress-spinner>

                <template v-if="results.attributes.length !== 0">
                    <md-table class="content" :value="results.attributes" md-sort="name" md-sort-order="asc" md-card>
                        <md-table-toolbar>
                            <div class="md-toolbar-section-start">
                                <h1 class="md-title">Результаты</h1>
                            </div>
                            <h1 class="md-toolbar-section-end">Корреляция: {{results.correlation}}</h1>
                        </md-table-toolbar>

                        <md-table-row slot="md-table-row" slot-scope="{ item }">
                            <md-table-cell md-label="ID" md-sort-by="id" md-numeric>{{ item.id }}</md-table-cell>
                            <md-table-cell md-label="Атрибут" md-sort-by="name">{{ item.name }}</md-table-cell>
                            <md-table-cell md-label="Текст 1" md-sort-by="text1" md-numeric>{{ item.first_text }}
                            </md-table-cell>
                            <md-table-cell md-label="Текст 2" md-sort-by="text2" md-numeric>{{ item.second_text }}
                            </md-table-cell>
                        </md-table-row>

                    </md-table>
                    <md-button class="md-raised md-primary" @click="setDone('third_step', 'results_step')">Продолжить
                    </md-button>
                </template>
            </md-step>
        </md-steppers>
    </div>
</template>

import $backend from '../backend'

<script>

import $backend from '../backend'

export default {
  name: 'MainScreen',
  data: () => ({
    active: 'first_step',
    first_step: false,
    second_step: false,
    third_step: false,
    results_step: false,
    first_text: '',
    second_text: '',
    attributes: {
      'avg_word_len': {name: 'Средняя длина слова (в буквах)', checked: true},
      'avg_sentence_len': {name: 'Средняя длина предложения (в словах)', checked: true},
      'sentence_len8_count': {
        name: 'Относительное оличество предложений длиннее 8-ми слов, %',
        checked: true
      },
      'flesch_kincaid_index': {name: 'Индекс удобочитаемости Флеша-Кинкейда', checked: true},
      'fog_index': {name: 'Индекс туманности Ганнинга', checked: true},
      'pr_coefficient': {name: 'Коэффициент предметности (Pr)', checked: true},
      'qu_coefficient': {name: 'Коэффициент качественности (Qu)', checked: true},
      'ac_coefficient': {name: 'Коэффициент активности (Ас)', checked: true},
      'din_coefficient': {name: 'Коэффициент динамизма (Din)', checked: true},
      'con_coefficient': {name: 'Коэффициент связности текста (Con)', checked: true}
    },
    results: {
      'correlation': null,
      'attributes': []
    }
  }),
  methods: {
    setDone (id, index) {
      this[id] = true
      if (index) {
        this.active = index
      }
      if (index === 'results_step') {
        this.getResults()
      }
    },
    getResults () {
      $backend.getResults({
        'first_text': this.first_text,
        'second_text': this.second_text,
        'attributes': this.attributes
      })
        .then(responseData => {
          this.results = responseData['results']
          console.log(this.results)
        }).catch(error => {
          this.error = error.message
        })
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
    h3 {
        margin: 40px 0 0;
    }

    ul {
        list-style-type: none;
        padding: 0;
    }

    li {
        display: inline-block;
        margin: 0 10px;
    }

    a {
        color: #42b983;
    }

    .content {
        padding: 20px;
    }

    .md-toolbar {
        margin-top: 16px;
        margin-bottom: 16px;
    }

    .md-progress-spinner {
        margin: 24px;
    }
</style>
