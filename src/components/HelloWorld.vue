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
                <md-button class="md-raised md-primary" @click="setDone('first_step', 'second_step')">Продолжить
                </md-button>
            </md-step>

            <md-step id="second_step" md-label="Второй текст" md-description="Обязательный шаг"
                     :md-done.sync="second_step">
                <md-field md-clearable>
                    <label>Введите второй текст</label>
                    <md-textarea v-model="second_text"></md-textarea>
                </md-field>
                <md-button class="md-raised md-primary" @click="setDone('second_step', 'third_step')">Продолжить
                </md-button>
            </md-step>

            <md-step id="third_step" md-label="Выбор атрибутов" md-description="Опциональный шаг"
                     :md-done.sync="third_step">
                <md-list>
                    <md-subheader>Выберите атрибуты</md-subheader>

                    <md-list-item>
                        <md-checkbox v-model="notification" value="preview"/>
                        <span class="md-list-item-text">Атрибут 1</span>
                    </md-list-item>

                    <md-list-item>
                        <md-checkbox v-model="notification" value="sound"/>
                        <span class="md-list-item-text">Атрибут 2</span>
                    </md-list-item>

                    <md-list-item>
                        <md-checkbox v-model="notification" value="vibrate"/>
                        <span class="md-list-item-text">Атрибут 3</span>
                    </md-list-item>

                    <md-list-item>
                        <md-checkbox v-model="notification" value="light"/>
                        <span class="md-list-item-text">Атрибут 4</span>
                    </md-list-item>
                </md-list>
                <md-button class="md-raised md-primary" @click="setDone('third_step', 'results_step')">Продолжить
                </md-button>
            </md-step>
            <md-step id="results_step" md-label="Результаты" md-description="Просмотр результатов"
                     :md-done.sync="results_step">
                <md-table class="content" v-model="results" md-sort="name" md-sort-order="asc" md-card>
                    <md-table-toolbar>
                        <h1 class="md-title">Результаты</h1>
                    </md-table-toolbar>

                    <md-table-row slot="md-table-row" slot-scope="{ item }">
                        <md-table-cell md-label="ID" md-sort-by="id" md-numeric>{{ item.id }}</md-table-cell>
                        <md-table-cell md-label="Атрибут" md-sort-by="name">{{ item.name }}</md-table-cell>
                        <md-table-cell md-label="Текст 1" md-sort-by="text1">{{ item.text1 }}</md-table-cell>
                        <md-table-cell md-label="Текст 2" md-sort-by="text2">{{ item.text2 }}</md-table-cell>
                    </md-table-row>
                </md-table>
                <md-button class="md-raised md-primary" @click="setDone('third_step', 'results_step')">Продолжить
                </md-button>
            </md-step>
        </md-steppers>
    </div>
</template>

<script>

export default {
  name: 'HelloWorld',
  data: () => ({
    active: 'first_step',
    first_step: false,
    second_step: false,
    third_step: false,
    results_step: false,
    first_text: '',
    second_text: '',
    results: [{id: 1, name: 'Атрибут1', text1: 323, text2: 344},
      {id: 2, name: 'Атрибут2', text1: 13, text2: 3},
      {id: 3, name: 'Атрибут3', text1: 2, text2: 4}]
  }),
  methods: {
    setDone (id, index) {
      this[id] = true

      if (index) {
        this.active = index
      }
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
</style>
