function generateProfileRadar(alignment_rep,
                              protein_rep,
                              motifs_rep,
                              rna_rep,
                              phylogeny_rep,
                              probability_rep) {
  var ctx = document.getElementById("my-chart").getContext('2d');
  var myChart = new Chart(ctx, {
    type: 'radar',
    data: {
      labels: ['Alignment', 'Protein', 'Motifs',
               'RNA', 'Phylogeny', 'Probability'],
      datasets: [{
        data: [alignment_rep, protein_rep, motifs_rep,
               rna_rep, phylogeny_rep, probability_rep]
      }]
    },
    options: {
      maintainAspectRatio: false,
    }
  });
};
