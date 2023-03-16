<template>
  <div class="text-center">
    <h1>Calendar</h1>
    <h2>{{ day }} / {{ month }} / {{ year }}</h2>
    <v-table fixed-header height="800px" weight="1000px">
      <thead>
        <tr>
          <th class="text-center">Hora</th>
          <th class="text-center" v-for="day in week" :key="day.id">
            <div v-if="day.id == this.day">
              <v-badge dot floating>
                {{ day.id }}
              </v-badge>
            </div>
            <div v-else>
              {{ day.id }}
            </div>
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="time in times" :key="time.time">
          <!--Hours-->
          <td>{{ time.time }}</td>
        <!--Days-->
          <td v-for="day in days" :key="day">
            <div v-for="date in dates" :key="date.id">
              <div
                v-if="date.weekDay == day && date.startTime == time.time"
              >
                <v-badge color="green" floating>
                    <v-card>
                        <v-card-title>{{ date.name }}</v-card-title>
                        <v-card-subtitle>{{ date.startTime }} - {{ date.enddTime }}</v-card-subtitle>
                    </v-card>
                </v-badge>
              </div>
            </div>
          </td>
        </tr>

      </tbody>
    </v-table>
  </div>
</template>

<style></style>

<script>
export default {
  name: "NewCalendar",
  props: {
    dates: Array,
  },
  data() {
    return {
      week: [],
      times: [],
      days: ["lunes", "martes", "miercoles", "jueves", "viernes", "sabado","domingo"],
    };
  },
  computed: {
    year() {
      return new Date().getFullYear();
    },
    month() {
      return new Date().getMonth();
    },
    day() {
      return new Date().getDate();
    },
  },
  methods: {
    getWeek() {
      var curr = new Date(); // get current date
      var first = curr.getDate() - curr.getDay(); // First day is the day of the month - the day of the week
      var last = first + 6; // last day is the first day + 6
      for (let i = first; i <= last; i++) {
        var day = new Date(curr.setDate(i)).toUTCString();
        const element = { day: day, id: i + 1 };
        this.week.push(element);
      }
    },
    //Get blocks of time of one hour
    getTimes() {
      var quarterHours = ["00", "15", "30", "45"];
      for (var i = 9; i < 20; i++) {
        for (var j = 0; j < 4; j++) {
          var time = i + ":" + quarterHours[j];
          if (i < 10) {
            time = "0" + time;
          }
          this.times.push({ time: time });
        }
      }
    },
  },
  created() {
    this.getWeek();
    this.getTimes();
  },
};
</script>
