#include "Drv_Timer.h"
#include "Timer.h"
#include "hw_ints.h"
//
#include "Ano_Scheduler.h"

void TIMER0B_Handler(void)
{
	/*清除中断标志*/
	ROM_TimerIntClear(TIMER0_BASE, TIMER_TIMB_TIMEOUT);
	/*原ICM20602的1ms中断*/
	INT_1ms_Task();	
	
}
void Drv_Timer0BInit(void)
{
	ROM_SysCtlPeripheralEnable(SYSCTL_PERIPH_TIMER0);
	/*配置定时器0B 1Ms*/
	ROM_TimerConfigure(TIMER0_BASE, TIMER_CFG_SPLIT_PAIR | TIMER_CFG_B_PERIODIC); 	 
	ROM_TimerPrescaleSet(TIMER0_BASE,  TIMER_B, 160-1);
	ROM_TimerLoadSet(TIMER0_BASE, TIMER_B, 500-1);
	/*开启定时器中断*/
	TimerIntRegister( TIMER0_BASE,  TIMER_B , TIMER0B_Handler);
	ROM_TimerIntEnable( TIMER0_BASE, TIMER_TIMB_TIMEOUT);
	ROM_TimerEnable( TIMER0_BASE, TIMER_TIMB_TIMEOUT );
	ROM_IntEnable( INT_TIMER0B );
}
