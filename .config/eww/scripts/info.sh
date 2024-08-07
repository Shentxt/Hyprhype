#!/bin/bash

info_mem () {
echo $(free -h | awk '/^Mem/ {print $3}' | sed 's/Gi//' | sed 's/,/./')
}

info_cpu () {
  PREV_TOTAL=0
PREV_IDLE=0
cpuFile="/tmp/.cpu_usage"

get_cpu() {
	if [[ -f "${cpuFile}" ]]; then
		fileCont=$(cat "${cpuFile}")
		PREV_TOTAL=$(echo "${fileCont}" | head -n 1)
		PREV_IDLE=$(echo "${fileCont}" | tail -n 1)
	fi

	CPU=(`cat /proc/stat | grep '^cpu '`) # Get the total CPU statistics.
	unset CPU[0]                          # Discard the "cpu" prefix.
	IDLE=${CPU[4]}                        # Get the idle CPU time.

	# Calculate the total CPU time.
	TOTAL=0

	for VALUE in "${CPU[@]:0:4}"; do
		let "TOTAL=$TOTAL+$VALUE"
	done

	if [[ "${PREV_TOTAL}" != "" ]] && [[ "${PREV_IDLE}" != "" ]]; then
		# Calculate the CPU usage since we last checked.
		let "DIFF_IDLE=$IDLE-$PREV_IDLE"
		let "DIFF_TOTAL=$TOTAL-$PREV_TOTAL"
		let "DIFF_USAGE=(1000*($DIFF_TOTAL-$DIFF_IDLE)/$DIFF_TOTAL+5)/10"
		echo "${DIFF_USAGE}"
	else
		echo "?"
	fi

	# Remember the total and idle CPU times for the next check.
	echo "${TOTAL}" > "${cpuFile}"
	echo "${IDLE}" >> "${cpuFile}"
}
get_cpu
}

info_disk () {
  df --output=pcent / | tail -n 1 | sed 's/%//g' | awk '{print $1}'
}

if [[ $1 == 'mem' ]]; then info_mem; fi
if [[ $1 == 'cpu' ]]; then info_cpu; fi
if [[ $1 == 'disk' ]]; then info_disk; fi
