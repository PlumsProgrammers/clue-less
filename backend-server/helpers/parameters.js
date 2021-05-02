/**
 * Checks if all the required params are present in the incoming request.
 *
 * @param {Request} req
 * @param {String[]} requiredParams
 * @return {Boolean} If all params are present in request
 */
exports.parameterCheck = (req, requiredParams) => {
  return requiredParams.every((param) => req.body.hasOwnProperty(param) && req.body[param] != null);
};

/**
 * Generates a proper english error message for the list of params.
 *
 * @param {String[]} requiredParams
 * @return {string} Error message with all required params listed.
 */
exports.paramsRequiredMessage = (requiredParams) => {
  if (requiredParams.length === 1) {
    return `${requiredParams[0]} is required.`;
  } else if (requiredParams.length === 2) {
    return `${requiredParams.join(' and ')} are required.`;
  } else {
    return `${requiredParams.slice(0, -1).join(', ')}, and ${requiredParams[requiredParams.length - 1]} are required.`;
  }
};
