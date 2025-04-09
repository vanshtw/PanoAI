USE [Panorama]
GO
/****** Object:  StoredProcedure [DX].[usp_GetChatBotData]    Script Date: 2025-03-17 08:51:43 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

ALTER   PROCEDURE [DX].[usp_GetChatBotData] @EntityKey BIGINT,
	@LevelName VARCHAR(50),
	@Ldap NVARCHAR(30)
AS
BEGIN
	SET NOCOUNT ON;

	DROP TABLE

	IF EXISTS #UserConfig;
		SELECT DISTINCT Ldap,
			ActionPage,
			TRY_CAST(CanEdit AS INT) AS CanEdit
		INTO #UserConfig
		FROM dxrpt.tm_user U(NOLOCK)
		JOIN dx.tlk_accessconfig AC(NOLOCK) ON AC.UserRole = U.UserRole
		WHERE U.Ldap = @Ldap
			AND ActionPage IN ('AccountHealth', 'SolutionHealth', 'RenewalScorecard', 'Alert', 'ShowFavorites', 'ShowHeirarchy', 'AddKBO', 'AddBio', 'AddUseCase')

	DROP TABLE

	IF EXISTS #PivotUserData;
		SELECT Ldap,
			[AccountHealth] AS [AccountHealth],
			[SolutionHealth] AS [SolutionHealth],
			[RenewalScorecard] AS [RenewalScorecard],
			[Alert] AS [Alert],
			[ShowFavorites] AS [ShowFavorites],
			[ShowHeirarchy] AS [ShowHeirarchy],
			[AddKBO] AS [AddKBO],
			[AddBio] AS [AddBio],
			[AddUseCase] AS [AddUseCase]
		INTO #PivotUserData
		FROM (
			SELECT *
			FROM #UserConfig
			) src
		PIVOT(SUM(CanEdit) FOR ActionPage IN (AccountHealth, SolutionHealth, RenewalScorecard, Alert, ShowFavorites, ShowHeirarchy, AddKBO, AddBio, AddUseCase)) pvt;

	DROP TABLE

	IF EXISTS #UsersSubKey
		SELECT DISTINCT SubKey
		INTO #UsersSubKey
		FROM DX.vw_tlkAccountHierarchy SP
		WHERE 1 = CASE WHEN @LevelName = 'TopParent' THEN CASE WHEN SP.TopParentKey = @EntityKey THEN 1 ELSE 0 END WHEN @LevelName = 'SubParent' THEN CASE WHEN SP.SubKey = @EntityKey THEN 1 ELSE 0 END WHEN @LevelName = 'Account' THEN CASE WHEN SP.AccountKey = @EntityKey THEN 1 ELSE 0 END WHEN @LevelName = 'EndUser' THEN CASE WHEN SP.EndUserKey = @EntityKey THEN 1 ELSE 0 END ELSE 0 END

	SELECT DISTINCT CJ.LevelName,
		CJ.EntityName,
		CJ.SubId,
		CJ.SubName,
		CJ.MarketArea,
		CJ.TopParentName,
		CJ.ReportingLevel,
		CJ.Solution,
		CJ.IsARR,
		CJ.ARRFlag,
		CJ.ARR_Formatted,
		CJ.IsPremierSupport,
		CJ.IsProvisioningData,
		CJ.NoofConsultingProjectsinYelloworRed,
		CJ.CustomerHealth,
		CJ.PredictiveHealth,
		CJ.PipelineOpportunitiesNos,
		CJ.PipelineOpportunitiesValue,
		CJ.NoofOpenTickets,
		CJ.OpenCaseAgeing,
		CJ.ClosedTickets,
		CJ.AverageResolutionDays,
		CJ.CSAT,
		CJ.TrainingUtilization,
		CJ.CritSit,
		CJ.CritSitStatus,
		CJ.ServiceEndDate,
		CJ.CurrentContractStartDate,
		CJ.Tenure,
		CJ.HandoffDate,
		CJ.IsHandoffAEtoOnboarding,
		CJ.AdoptionScore,
		CJ.AdoptionScoreCYStart,
		CJ.AdoptionScoreTrend,
		CJ.ContractualUtilization,
		CJ.ContractualUtilization_ForPPT,
		CJ.ContractualUtilizationNumber,
		CJ.RBoB,
		CJ.RBoBFormatted,
		CJ.Outlook,
		CJ.OutlookFormatted,
		CJ.NoRenewalScorecardCompleted,
		CJ.NoRenewalScorecardTotal,
		CJ.RenewalScorecardCompletion,
		CJ.IsRenewalAtRisk,
		CJ.IsUpsellExpected,
		CJ.IsRiskReasonCodesUpdated,
		CJ.IsCriticalContactIdentified,
		CJ.CompetitorThreat,
		CJ.ConsultingUtilization,
		CJ.MaturityAssessmentActual,
		CJ.SBRActual,
		CJ.MSPActual,
		CJ.ValueSummaryPillar,
		CJ.ValueSummaryLastUpdatedOn,
		CJ.ValueSummaryStatus,
		CJ.ValueSummaryActual,
		CJ.IsRunAndOperatePartner,
		CJ.IsImplementationPartner,
		CJ.IsUpsellCrosssellIndicator,
		CJ.ImplementationHealth,
		CJ.ConsultingBacklog,
		CJ.TrainingBacklog,
		CJ.NextRenewalQtr,
		CJ.CoverageModel,
		CJ.ETLLoadDate,
		CJ.PremierSupportLevel,
		CJ.IsValidforDashboard,
		CJ.EscalatedTickets,
		CJ.TAMHealth,
		CJ.ServicePeriod,
		CJ.ServiceReviewDate,
		CJ.ServiceDeliveryPlanDate,
		CJ.PaidSupportCSAT,
		CJ.PaidSupportARR_Formatted,
		CJ.SDPSharepointLink,
		CJ.OLIContractStartDate,
		CJ.IsTAMCompliant,
		CJ.IsKickOffCompliant,
		CJ.IsMAPCompliant,
		CJ.IsServiceReviewCompliant,
		CJ.NoofKBOs,
		CJ.KickOffCompliantLastDate,
		CJ.MAPCompliantLastDate,
		CJ.ServiceReviewCompliantLastDate,
		CJ.PackageType,
		CJ.IsValidforTAMDashboard,
		CJ.ForcastExtendedPriceUSD,
		CJ.UseCases,
		CJ.ConsultingBooking_Formatted,
		CJ.HasPaidsupport
	-- ProjectID,  
	-- AccountID,  
	-- SFDCRole,  
	-- JobRoleName,  
	-- PanoramaStatus,  
	-- U.Email,  
	-- U.EmployeeName,  
	-- U.UserRole,  
	-- U.HasARRAccess  
	-- PU.*  
	FROM DX.vw_txCustomerJourneySteps CJ(NOLOCK)
	--LEFT JOIN dx.vw_UPSProjectAssignments PA(NOLOCK) ON PA.SubKey = CJ.SubKey  
	-- LEFT JOIN dxrpt.tm_user U(NOLOCK) ON PA.Ldap = U.Ldap  
	--LEFT JOIN #PivotUserData PU ON PU.Ldap = U.Ldap  
	WHERE LevelName = @LevelName
		AND EntityKey = @EntityKey

	SELECT PSProjectId,
		PSProjectName,
		ProjectStatus,
		ProjectPlannedStartDate,
		ProjectPlannedEndDate,
		ProjectActualStartDate,
		ProjectActualEndDate,
		ProjectPeriod,
		KickOffCompliant,
		KickOffDate,
		SRCompliant,
		SRDate,
		MAPCompliant,
		MAPDate,
		IsActiveProject,
		IsNonPaidEngagement
	FROM Panorama.dx.vw_txPSProject(NOLOCK)
	WHERE SubKey = @EntityKey

	SELECT DISTINCT PSTaskId,
		PSProjectid,
		ProjectName,
		ActivityType,
		StartDate,
		CompletionDate,
		PrimaryOwnerName,
		Collaborators,
		PanoramaStatus AS ActivityStatus
	FROM Panorama.dx.vw_txPSActivities(NOLOCK)
	WHERE SubKey = @EntityKey

	--SELECT * from #UsersSubKey  
	SELECT DISTINCT ProjectID,
		AccountID,
		SFDCRole,
		JobRoleName,
		PanoramaStatus,
		U.Email,
		U.EmployeeName,
		CASE WHEN U.UserRole = 'USN_CSM' THEN 'Named CSM' WHEN U.UserRole = 'USS_CSM' THEN 'Solution CSM' ELSE U.UserRole END AS 'UserRole',
		U.HasARRAccess,
		PU.*
	FROM dxrpt.tm_user U(NOLOCK)
	JOIN #PivotUserData PU ON PU.Ldap = U.Ldap
	LEFT JOIN dx.vw_UPSProjectAssignments PA(NOLOCK) ON PA.Ldap = U.Ldap
	LEFT JOIN #UsersSubKey USK ON USK.SubKey = PA.SubKey
END
