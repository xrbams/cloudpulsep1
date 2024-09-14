
const { BigQuery } = require('@google-cloud/bigquery');

// Create a BigQuery client
const bigQueryClient = new BigQuery({
  projectId: 'smart-charter-422809-k0',
  keyFilename: './smart-charter-422809-k0-c14110680e9e.json'
});

const datasetId = 'sports_data';

module.exports = {
  bigQueryClient,
  datasetId
};
