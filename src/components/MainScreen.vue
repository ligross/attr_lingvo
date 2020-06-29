<template>
    <div class="content">
        <template v-if="selected !== null">
            <md-dialog :md-active.sync="showDialog" md-click-outside-to-close>
                <md-dialog-title>
                    <div class="md-layout md-gutter md-alignment-center-center">
                        <div class="md-layout-item">
                            {{ selected.description}}
                        </div>
                        <div class="md-layout md-alignment-center-right">
                            <md-button class="md-primary md-layout-item md-size-15" @click="showDialog = false">
                                <md-icon>close</md-icon>
                            </md-button>
                        </div>
                    </div>
                </md-dialog-title>
                <md-dialog-content>
                    <md-tabs>
                        <md-tab id="text1" md-label="Текст 1" class="md-scrollbar">
                            <div v-bind:key='item.id' v-for="item in selected.first_text.debug" class="md-scrollbar">
                                <p v-html="item">{{ item }}</p>
                            </div>
                        </md-tab>
                        <md-tab id="text2" md-label="Текст 2" class="md-scrollbar">
                            <div v-bind:key='item.id' v-for="item in selected.second_text.debug" class="md-scrollbar">
                                <p v-html="item">{{ item }}</p>
                            </div>
                        </md-tab>
                    </md-tabs>
                </md-dialog-content>
            </md-dialog>
        </template>
        <md-toolbar class="md-transparent">
            <div class="md-toolbar-row">
                <h3 class="md-title">Тут какое-то название или описание</h3>
            </div>
        </md-toolbar>

        <md-steppers :md-active-step.sync="active" md-linear>
            <md-step id="first_step" md-label="Первый текст" md-description="Обязательный шаг"
                     :md-done.sync="first_step">
                <div class="md-layout md-gutter md-alignment-center-center">
                    <div class="md-layout-item">
                        <md-field id="firstTextGenre">
                            <label for="firstTextGenre">Жанр</label>
                            <md-select v-model="firstTextGenre" name="firstTextGenre">
                                <md-option v-for="genre in genres" v-bind:value="genre.value" :key="genre.value">{{
                                    genre.text }}
                                </md-option>
                            </md-select>
                        </md-field>
                    </div>
                </div>
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
                <div class="md-layout md-gutter md-alignment-center-center">
                    <div class="md-layout-item">
                        <md-field id="secondTextGenre">
                            <label for="secondTextGenre">Жанр</label>
                            <md-select v-model="secondTextGenre" name="secondTextGenre">
                                <md-option v-for="genre in genres" v-bind:value="genre.value" :key="genre.value">{{
                                    genre.text }}
                                </md-option>
                            </md-select>
                        </md-field>
                    </div>
                </div>
                <md-field md-clearable>
                    <label>Введите второй текст</label>
                    <md-textarea v-model="second_text"></md-textarea>
                </md-field>
                <md-button class="md-raised md-primary" :disabled="!second_text"
                           @click="setDone('second_step', 'third_step')">Продолжить
                </md-button>
            </md-step>

            <md-step id="third_step" class="md-layout md-gutter md-alignment-center" md-label="Выбор атрибутов"
                     md-description="Опциональный шаг"
                     :md-done.sync="third_step">
                <div class="md-layout md-gutter" style="justify-content:center">
                    <div class="viewport">
                        <md-list>
                            <md-subheader>Стилостатистика</md-subheader>
                            <md-list-item :key="attributes.flesch_kincaid_index.name">
                                <md-checkbox v-model="attributes.flesch_kincaid_index.checked"/>
                                <span class="md-list-item-text">{{ attributes.flesch_kincaid_index.name }}</span>
                            </md-list-item>
                            <md-list-item :key="attributes.fog_index.name">
                                <md-checkbox v-model="attributes.fog_index.checked"/>
                                <span class="md-list-item-text">{{ attributes.fog_index.name }}</span>
                            </md-list-item>
                            <md-divider></md-divider>
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
                            <md-divider></md-divider>
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
                            <md-divider></md-divider>
                            <md-list-item :key="attributes.errors.name">
                                <md-checkbox v-model="attributes.errors.checked"/>
                                <span class="md-list-item-text">{{ attributes.errors.name }}</span>
                            </md-list-item>
                        </md-list>
                    </div>
                    <div class="viewport">
                        <md-list>
                            <md-subheader>Стилостатистика с когнитивной базой</md-subheader>
                            <md-list-item :key="attributes.uniform_rows_count.name">
                                <md-checkbox v-model="attributes.uniform_rows_count.checked"/>
                                <span class="md-list-item-text">{{ attributes.uniform_rows_count.name }}</span>
                            </md-list-item>
                            <md-list-item :key="attributes.introductory_words_count.name">
                                <md-checkbox v-model="attributes.introductory_words_count.checked"/>
                                <span class="md-list-item-text">{{ attributes.introductory_words_count.name }}</span>
                            </md-list-item>
                            <md-list-item :key="attributes.comparatives_count.name">
                                <md-checkbox v-model="attributes.comparatives_count.checked"/>
                                <span class="md-list-item-text">{{ attributes.comparatives_count.name }}</span>
                            </md-list-item>
                            <md-list-item :key="attributes.syntax_splices_count.name">
                                <md-checkbox v-model="attributes.syntax_splices_count.checked"/>
                                <span class="md-list-item-text">{{ attributes.syntax_splices_count.name }}</span>
                            </md-list-item>
                            <md-list-item :key="attributes.comparative_clauses_count.name">
                                <md-checkbox v-model="attributes.comparative_clauses_count.checked"/>
                                <span class="md-list-item-text">{{ attributes.comparative_clauses_count.name }}</span>
                            </md-list-item>
                            <md-list-item :key="attributes.collation_clauses_count.name">
                                <md-checkbox v-model="attributes.collation_clauses_count.checked"/>
                                <span class="md-list-item-text">{{ attributes.collation_clauses_count.name }}</span>
                            </md-list-item>
                            <md-list-item :key="attributes.epenthetic_constructions_count.name">
                                <md-checkbox v-model="attributes.epenthetic_constructions_count.checked"/>
                                <span class="md-list-item-text">{{ attributes.epenthetic_constructions_count.name }}</span>
                            </md-list-item>
                            <md-list-item :key="attributes.complex_syntax_constructs_count.name">
                                <md-checkbox v-model="attributes.complex_syntax_constructs_count.checked"/>
                                <span class="md-list-item-text">{{ attributes.complex_syntax_constructs_count.name }}</span>
                            </md-list-item>
                            <md-list-item :key="attributes.single_verb_count.name">
                                <md-checkbox v-model="attributes.single_verb_count.checked"/>
                                <span class="md-list-item-text">{{ attributes.single_verb_count.name }}</span>
                            </md-list-item>
                            <md-list-item :key="attributes.appeal_count.name">
                                <md-checkbox v-model="attributes.appeal_count.checked"/>
                                <span class="md-list-item-text">{{ attributes.appeal_count.name }}</span>
                            </md-list-item>
                        </md-list>
                    </div>
                    <div class="viewport">
                        <md-list>
                            <md-subheader>Описание тезауруса личности</md-subheader>
                            <md-list-item :key="attributes.dichotomy_pronouns_count.name">
                                <md-checkbox v-model="attributes.dichotomy_pronouns_count.checked"/>
                                <span class="md-list-item-text">{{ attributes.dichotomy_pronouns_count.name }}</span>
                            </md-list-item>
                        </md-list>
                    </div>
                    <div class="viewport">
                        <md-list>
                            <md-subheader>Вербально-семантический уровень</md-subheader>
                            <md-list-item :key="attributes.complex_words_count.name">
                                <md-checkbox v-model="attributes.complex_words_count.checked"/>
                                <span class="md-list-item-text">{{ attributes.complex_words_count.name }}</span>
                            </md-list-item>
                            <md-list-item :key="attributes.modal_particles_count.name">
                                <md-checkbox v-model="attributes.modal_particles_count.checked"/>
                                <span class="md-list-item-text">{{ attributes.modal_particles_count.name }}</span>
                            </md-list-item>
                            <md-list-item :key="attributes.interjections_count.name">
                                <md-checkbox v-model="attributes.interjections_count.checked"/>
                                <span class="md-list-item-text">{{ attributes.interjections_count.name }}</span>
                            </md-list-item>
                            <md-list-item :key="attributes.modal_postfix_count.name">
                                <md-checkbox v-model="attributes.modal_postfix_count.checked"/>
                                <span class="md-list-item-text">{{ attributes.modal_postfix_count.name }}</span>
                            </md-list-item>
                            <md-list-item :key="attributes.intensifiers_count.name">
                                <md-checkbox v-model="attributes.intensifiers_count.checked"/>
                                <span class="md-list-item-text">{{ attributes.intensifiers_count.name }}</span>
                            </md-list-item>
                        </md-list>
                    </div>
                </div>
                <div class="md-layout md-gutter md-alignment-center">
                    <md-button class="md-raised md-primary" :disabled="noAttributesSelected()"
                               @click="setDone('third_step', 'results_step')">Продолжить
                    </md-button>
                </div>
            </md-step>
            <md-step id="results_step" md-label="Результаты" md-description="Просмотр результатов"
                     :md-done.sync="results_step">

                <md-progress-spinner v-if="is_processing" :md-diameter="100" :md-stroke="10"
                                     md-mode="indeterminate"></md-progress-spinner>
                <md-empty-state
                        v-if='this.error && !this.is_processing'
                        md-icon="power_off"
                        md-label="Что-то пошло не так..."
                        md-description="Пожалуйста, повторите запрос">
                    <md-button class="md-raised md-primary" @click="setDone('third_step', 'results_step')">Повторить
                    </md-button>
                </md-empty-state>

                <template v-if="results.attributes.length !== 0">
                    <md-tabs class="md-primary" style="padding: 20px">
                        <md-tab id="results" md-label="Результаты">
                            <md-table class="content" :value="results.attributes" md-sort="id" md-sort-order="asc"
                                      md-fixed-header
                                      md-card>
                                <md-table-toolbar>
                                    <div class="md-toolbar-section-start">
                                        <h1 class="md-title">Корреляция: {{results.correlation}}</h1>
                                    </div>
                                </md-table-toolbar>

                                <md-table-row slot="md-table-row" slot-scope="{ item }">
                                    <md-table-cell md-label="ID" md-sort-by="id" md-numeric>{{ item.id }}
                                    </md-table-cell>
                                    <md-table-cell md-label="Атрибут" md-sort-by="name">{{ item.name }}</md-table-cell>
                                    <md-table-cell md-label="Текст 1" md-sort-by="text1" md-numeric>{{ item.first_text
                                        }}
                                    </md-table-cell>
                                    <md-table-cell md-label="Текст 2" md-sort-by="text2" md-numeric>{{ item.second_text
                                        }}
                                    </md-table-cell>
                                </md-table-row>

                            </md-table>
                        </md-tab>
                        <md-tab id="extended" md-label="Вспомогательные параметры">
                            <md-table class="content" :value="results.extended_attributes" md-sort="id"
                                      md-sort-order="asc"
                                      md-fixed-header
                                      md-card>
                                <md-table-row slot="md-table-row" slot-scope="{ item }" @click.native="onSelect(item)">
                                    <md-table-cell md-label="ID" md-sort-by="id" md-numeric>{{ item.id }}
                                    </md-table-cell>
                                    <md-table-cell md-label="Атрибут" md-sort-by="name">{{ item.description }}
                                    </md-table-cell>
                                    <md-table-cell md-label="Текст 1" md-sort-by="text1" md-numeric>{{
                                        item.first_text['value'] }}
                                    </md-table-cell>
                                    <md-table-cell md-label="Текст 2" md-sort-by="text2" md-numeric>{{
                                        item.second_text['value'] }}
                                    </md-table-cell>
                                    <md-table-cell md-label="Просмотр">
                                        <md-icon v-if="item.first_text.debug && item.first_text.debug.length > 0">
                                            visibility
                                        </md-icon>
                                        <md-icon v-if="!item.first_text.debug || item.first_text.debug.length === 0">
                                            visibility_off
                                        </md-icon>
                                    </md-table-cell>
                                </md-table-row>
                            </md-table>
                        </md-tab>
                    </md-tabs>

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
    showDialog: false,
    selected: null,
    is_processing: true,
    error: '',
    active: 'first_step',
    first_step: false,
    second_step: false,
    third_step: false,
    results_step: false,
    first_text: '',
    second_text: '',
    firstTextGenre: 'fiction',
    secondTextGenre: 'fiction',
    genres: [
      {text: 'художественная проза', value: 'fiction'},
      {text: 'сетевая литература', value: 'online_literature'},
      {text: 'сетевая публицистика', value: 'online_journalism'},
      {text: 'сетевая развлекательная публицистика', value: 'online_entertainment_journalism'},
      {text: 'корпоративная переписка', value: 'corporate_correspondence'}
    ],
    attributes: {
      'avg_word_len': {name: 'Средняя длина слова (в буквах)', checked: true},
      'avg_sentence_len': {name: 'Средняя длина предложения (в словах)', checked: true},
      'sentence_len8_count': {
        name: 'Количество предложений длиннее 8-ми слов',
        checked: true
      },
      'flesch_kincaid_index': {name: 'Индекс удобочитаемости Флеша-Кинкейда', checked: true},
      'fog_index': {name: 'Индекс туманности Ганнинга', checked: true},
      'pr_coefficient': {name: 'Коэффициент предметности (Pr)', checked: true},
      'qu_coefficient': {name: 'Коэффициент качественности (Qu)', checked: true},
      'ac_coefficient': {name: 'Коэффициент активности (Ас)', checked: true},
      'din_coefficient': {name: 'Коэффициент динамизма (Din)', checked: true},
      'con_coefficient': {name: 'Коэффициент связности текста (Con)', checked: true},
      'errors': {name: 'Количество орфографических ошибок', checked: true},
      'uniform_rows_count': {name: 'Предложения с однородными рядами', checked: true},
      'introductory_words_count': {name: 'Вводные слова и конструкции', checked: true},
      'comparatives_count': {name: 'Целевые, выделительные и сравнительные обороты', checked: true},
      'syntax_splices_count': {name: 'Синтаксические сращения', checked: true},
      'comparative_clauses_count': {name: 'Сравнительные придаточные', checked: true},
      'collation_clauses_count': {name: 'Сопоставительные придаточные', checked: true},
      'epenthetic_constructions_count': {name: 'Вставные конструкции', checked: true},
      'complex_syntax_constructs_count': {name: 'Сложные синтаксические конструкции', checked: true},
      'single_verb_count': {name: 'Глагольные односоставные предложения', checked: true},
      'appeal_count': {name: 'Обращения', checked: true},
      'dichotomy_pronouns_count': {name: 'Дихотомия "свой/чужой"', checked: true},
      'complex_words_count': {name: 'Сложные слова полуслитного написания', checked: true},
      'modal_particles_count': {name: 'Модальные частицы', checked: true},
      'interjections_count': {name: 'Междометия', checked: true},
      'modal_postfix_count': {name: 'Наличие/отсутствие модального постфикса «-то»', checked: true},
      'intensifiers_count': {name: 'Предпочтительные слова-интенсификаторы', checked: true}
    },
    results: {
      'correlation': null,
      'attributes': [],
      'extended_attributes': []
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
    noAttributesSelected () {
      return Object.keys(this.attributes).filter(key => this.attributes[key]['checked'] === true).length === 0
    },
    onSelect (item) {
      console.log(item)
      if (item !== undefined && (item.first_text.debug || item.second_text.debug)) {
        this.selected = item || this.selected
        this.showDialog = true
      }
    },
    getResults () {
      this.error = ''
      this.is_processing = true
      this.results = {
        'correlation': null,
        'attributes': [],
        'extended_attributes': []
      }
      $backend.getResults({
        'first_text': this.first_text,
        'first_text_genre': this.first_text_genre,
        'second_text': this.second_text,
        'second_text_genre': this.second_text_genre,
        'attributes': this.attributes
      })
        .then(responseData => {
          this.results = responseData['results']
          console.log(this.results)
          this.is_processing = false
          console.log(this.results)
        }).catch(error => {
          this.is_processing = false
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

    .viewport {
        width: 500px;
        max-width: 100%;
        display: inline-block;
        vertical-align: top;
        overflow: auto;
        padding-top: 30px;
        border: 1px solid rgba(#000, .12);

    }
</style>

<style lang="css">
    .md-menu-content.md-select-menu {
        width: auto;
        max-width: none;
    }
</style>
