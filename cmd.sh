################################################################################
# Help                                                                         #
################################################################################
Help()
{
   # Display Help
   echo "Add description of the script functions here."
   echo
   echo "Syntax: cmd.sh [start_dev | stop_dev | start_prod | stop_prod | rebuild_dev | help]"
   echo "options:"
   echo "start_dev     Start development docker compose."
   echo "stop_dev      Stop development docker compose."
   echo "start_prod    Start production docker compose."
   echo "stop_prod     Stop production docker compose."
   echo "rebuild_dev   rebuild development docker image."
   echo
}

################################################################################
################################################################################
# Main program                                                                 #
################################################################################
################################################################################

# Get the options
while true; do
   case $1 in
      help) # display Help
         Help
         exit;;
      start_dev)
         cd compose/dev
         docker compose up -d
         exit;;
      start_prod)
         cd compose/prod
         docker compose up -d
         exit;;
      stop_dev)
         cd compose/dev
         docker compose down
         exit;;
      restart_dev)
         cd compose/dev
         docker compose down
         docker compose up -d
         exit;;
      rebuild_dev)
         cd compose/dev
         docker compose down
         docker image rm dev-app 
         docker compose up -d
         exit;;
      stop_prod)
         cd compose/prod
         docker compose down
         exit;;
      *) # incorrect option
         echo "Error: Invalid option"
         Help
         exit;;
   esac
done