var lcViewerInterface = new LibCrowdsViewerInterface({ 
  id: 'viewer', 
  selectionEnabled: true
});

/**
 * Load the task.
 */
pybossa.taskLoaded(function(task, deferred) {
  deferred.resolve(task);
  lcViewerInterface.updatePreview(task.info.image_ark);
});

/**
 * Present the task.
 */
pybossa.presentTask(function(task, deferred) {
    if (!$.isEmptyObject(task)) {
        
        pybossa.userProgress('{{ short_name }}').done(function(data){
            lcViewerInterface.updateUserProgress(data);
        });
  
        lcViewerInterface.viewer.addHandler('open', function() {
    if(typeof task.info.region !== 'undefined') {
      lcViewerInterface.highlight(task.info.region);
    }
  });
        
  lcViewerInterface.loadTask(task);
  
        $('.btn-answer').off('click').on('click', function() {
            task.answer = {
                category: task.info.category,
                comment: lcViewerInterface.getComments(),
                image_ark: task.info.image_ark,
                manifest_id: task.info.manifest_id,
                regions: lcViewerInterface.getSelections()
            };
            
            console.log(JSON.stringify(task.answer, null, 2));
            
            pybossa.saveTask(task.id, task.answer).done(function() {
                deferred.resolve();
                notify('Answer saved, thanks!', 'success');
                lcViewerInterface.clearTask();
            }).fail(function(xhr, status, error) {
                notify(status, 'error')
                throw new Error(error);
            });
        });
    } else {
      $("#project-content").hide();
      notify('Congratulations! You have contributed to all available tasks!', 'success');
    }
  });
  pybossa.run('{{ short_name }}');