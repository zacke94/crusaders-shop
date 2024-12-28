const ToastService = {
  /**
   * @param toastInstance {any}
   * @returns {void}
   */
  showError(toastInstance) {
    toastInstance.add({
      severity: 'error',
      summary: 'Något gick fel',
      detail: 'Skrik på Adam',
      life: 6000
    });
  },

  /**
   * @param toastInstance {any}
   * @param message {string}
   * @returns {void}
   */
  showSuccess(toastInstance, message) {
    toastInstance.add({
      severity: 'success',
      summary: message,
      life: 6000
    });
  }
};

export default ToastService;
