# Tips for kubectl

- to switch between multiple cluster with individual kubeconfig,  by configuring `$KUBECONFIG` environment variable to specify multiple kubeconfig files separated by using colons. It should look like that when you have multiple config files:

    ```sh
    export $KUBECONFIG=/Users/aguedes/.kube/contexts/kubeconfig-cluster-1.yml:/Users/aguedes/.kube/contexts/kubeconfig-cluster-2.yml
    ```

    we can add this environment to ~/.bashrc or ~/.zshrc

    also we need to install plugin [kubectx](https://github.com/ahmetb/kubectx), when we can switch different cluster and context
