const { client, index, type } = require('./connection')

module.exports = {
  /** Query ES index for the provided term , match to a field if given*/
  queryTerm (term, match_term = '', offset = 0) {
    const body = {
      from: offset,
      query: {}
    };

    // Check if field to match to is given
    if (match_term != '') {
        body.query['match'] = {};
        body.query.match[match_term] = {
              query: term,
              fuzziness: 'auto'
        };
    }
    else {
        body.query['query_string'] = {
              query: term,
              fuzziness: 'auto'
        };
    }

    return client.search({ index, type, body })
  }
}