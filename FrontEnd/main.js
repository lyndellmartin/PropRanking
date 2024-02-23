import { updateNBA } from "/PropRanking-main/main.py";

function generateStats() {
  document.getElementById("sotwPopup").hidden = true;
  updateNBA();
}
