<script setup>
import { RouterLink, RouterView } from "vue-router";
</script>

<template>
  <v-app>
      <h1>Prueba frontend con Vue 3</h1>
      <div>
        <v-breadcrumbs :items="items" divider="-"></v-breadcrumbs>
      </div>
      <RouterView :dates="dates" />

  </v-app>
</template>
<script>
export default {
  data: () => ({
    items: [
      {
        title: "Home",
        disabled: false,
        href: "/",
      },
      {
        title: "Calendar made in Vue3 + HTML + CSS",
        disabled: false,
        href: "calendarCSS",
      },
    ],
    dates: [
      {
        id: 0,
        name: "Sofía González",
        weekDay: "lunes",
        startTime: "10:30",
        enddTime: "11:00",
      },
      {
        id: 1,
        name: "Santiago Morales",
        weekDay: "martes",
        startTime: "12:30",
        enddTime: "14:30",
      },
      {
        id: 2,
        name: "Ana Herrera",
        weekDay: "miercoles",
        startTime: "16:00",
        enddTime: "16:15",
      },
      {
        id: 3,
        name: "Luisa Gutiérrez",
        weekDay: "jueves",
        startTime: "15:45",
        enddTime: "16:30",
      },
      {
        id: 4,
        name: "Carlos Castro",
        weekDay: "viernes",
        startTime: "18:45",
        enddTime: "19:45",
      },
      {
        id: 5,
        name: "Valentina Flores",
        weekDay: "martes",
        startTime: "14:30",
        enddTime: "15:00",
      },
      {
        id: 6,
        name: "Pablo Hernández",
        weekDay: "viernes",
        startTime: "14:30",
        enddTime: "15:30",
      },
      {
        id: 7,
        name: "Juan Soto",
        weekDay: "lunes",
        startTime: "17:30",
        enddTime: "18:30",
      },
    ],
  }),
};
</script>
