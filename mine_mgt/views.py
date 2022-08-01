from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import Claim, Proof, Payment, AnnualInspection
from accounts.models import User
from .forms import ProofForm, ClaimForm, PaymentForm, MonthlyReturnForm, PaymentClaimForm, AnnualInspectionForm, ReasonForm


@login_required
def dashboard(request):
    forfeited_claims = Claim.forfeited.all()

    if request.user.is_mine:
        active_claims = Claim.active.filter(applicant=request.user)
        pending_claims = Claim.pending_approval.filter(applicant=request.user)
        declined_claims = Claim.declined.filter(applicant=request.user)
        user = get_object_or_404(User, id=request.user.id)
        balance = 0
        monthly_labour_returns = 0
        for mine in request.user.claims.all():
            balance += mine.balance
            monthly_labour_returns += mine.monthly_labour_returns
        context = {
            'active_claims': active_claims,
            'pending_claims': pending_claims,
            'user': user,
            'forfeited_claims': forfeited_claims,
            'balance': balance,
            'monthly_labour_returns': monthly_labour_returns,
            'declined_claims': declined_claims
        }
        
        
        return render(request, 'mine_mgt/miner/dashboard.html', context)
    else:
        active_claims = Claim.active.filter()
        pending_claims = Claim.pending_approval.filter()
        proofs = Proof.objects.exclude(is_processeed=True)
        total_output = 0
        for claim in active_claims:
            total_output += claim.monthly_labour_returns
        context = {
            'active_claims': active_claims,
            'pending_claims': pending_claims,
            'forfeited_claims': forfeited_claims,
            'proofs': proofs,
            'total_output': total_output
        }
        return render(request, 'mine_mgt/admin/dashboard.html', context)


@login_required
def payments(request):
    if request.user.is_mine:
        balance = 0
        monthly_labour_returns = 0
        for mine in request.user.claims.all():
            balance += mine.balance
            monthly_labour_returns += mine.monthly_labour_returns

        if request.method == 'POST':
            form = ProofForm(data=request.POST, files=request.FILES)
            if form.is_valid():
                new_proof = form.save(commit=False)
                new_proof.uploaded_by = get_object_or_404(User, id=request.user.id)
                new_proof.save()
                return redirect('mine_mgt:payments')
        else:
            form = ProofForm()

        payments = Payment.objects.filter(user=request.user)
        proofs = Proof.objects.filter(uploaded_by=request.user)
        context = {
            'payments': payments,
            'proofs': proofs,
            'form': form,
            'balance': balance
        }
        return render(request, 'mine_mgt/miner/payments.html', context)
    else:
        payments = Payment.objects.all()
        balance = 0
        for payment in payments:
            balance += int(payment.amount)
        proofs = Proof.objects.exclude(is_processeed=True)
        context = {
            'payments': payments,
            'proofs': proofs,
            'balance': balance
        }
        return render(request, 'mine_mgt/admin/payments.html', context)



@login_required
def claim_detail(request, id):
    if request.user.is_administrator:
        claim = get_object_or_404(Claim, id=id)
        proofs = Proof.objects.filter(uploaded_by=request.user)
        payments = claim.invoices.all()
        if request.method == 'POST':
            form = ReasonForm(request.POST)
            if form.is_valid():
                claim.status = 'forfeit'
                claim.reason = form.get_info()
                claim.save()
                return redirect('mine_mgt:dashboard')
        else:
            form = ReasonForm()
        context = {
            'claim': claim,
            'proofs': proofs,
            'payments': payments,
            'form': form
        }
        

        return render(request, 'mine_mgt/admin/claim_detail.html', context)
    else:
        claim = get_object_or_404(Claim, id=id)
        payments = claim.invoices.all()
        context = {
            'claim': claim,
            'payments': payments
        }
        return render(request, 'mine_mgt/miner/claim_detail.html', context)


@login_required
def claim_application(request, id):
    if request.user.is_administrator:
        claim = get_object_or_404(Claim, id=id)
        if request.method == 'POST':
            form = MonthlyReturnForm(request.POST)
            if form.is_valid():
                claim.balance -= int(form.get_info())
                claim.monthly_labour_returns = int(form.get_info())
                claim.status = 'active'
                claim.save()
                return redirect('mine_mgt:dashboard')
        else:
            form = MonthlyReturnForm()
        
        pending_claims = Claim.pending_approval.exclude(id=id)
        context = {
            'claim': claim,
            'pending_claims': pending_claims,
            'form': form
        }
        return render(request, 'mine_mgt/admin/claim_application.html', context)
    else:
        return redirect('mine_mgt:dashboard')

@login_required
def accept(request, id):
    claim = get_object_or_404(Claim, id=id)
    if request.method == 'POST':
        form = MonthlyReturnForm(request.POST)
        # if form.is_valid():
        #     form.send(product.user.email, url)
        #     return redirect('products:product_list')
    else:
        form = MonthlyReturnForm()

    claim.status = 'active'
    claim.save()
    return redirect('mine_mgt:dashboard')

@login_required
def apply(request):
    claims = Claim.forfeited.all()
    if request.method == 'POST':
        form = ClaimForm(data=request.POST)
        if form.is_valid():
            new_claim = form.save(commit=False)
            new_claim.applicant = get_object_or_404(User, id=request.user.id)
            new_claim.save()
            return redirect('mine_mgt:dashboard')
    else:
        form = ClaimForm()

    context = {
        'claims': claims,
        'form': form
    }
    return render(request, 'mine_mgt/miner/apply.html', context)


@login_required
def apply_forfeited(request, id):
    claim = Claim.forfeited.get(id=id)
    claim.applicant = get_object_or_404(User, id=request.user.id)
    claim.status = 'pending_approval'
    claim.save()
    return redirect('mine_mgt:dashboard')

@login_required
def delete_forfeited(request, id):
    claim = Claim.forfeited.get(id=id)
    claim.delete()
    return redirect('mine_mgt:dashboard')

@login_required
def forfeited(request, id):
    claim = Claim.forfeited.get(id=id)
    claims = Claim.forfeited.exclude(id=id)
    context = {
        'claim': claim,
        'claims': claims
    }

    return render(request, 'mine_mgt/miner/forfeited.html', context)



@login_required
def add_payment(request, id):
    proof = get_object_or_404(Proof, id=id)
    userr = proof.uploaded_by
    if request.method == 'POST':
        form = PaymentForm(data=request.POST, user=userr)
        if form.is_valid():
            new_payment = form.save(commit=False)
            new_payment.user = get_object_or_404(User, id=proof.uploaded_by.id)
            new_payment.proof = proof
            new_payment.is_processeed = True
            print('434343434343434333334343', new_payment)
            new_payment.save()
            claim = form.cleaned_data['claim']
            claim.balance += int(form.cleaned_data['amount'])
            claim.save()
            proof.is_processeed = True
            proof.save()
            return redirect('mine_mgt:dashboard')
    else:
        form = PaymentForm(user=userr)

    context = {
        'proof': proof,
        'form': form,
        'userr': userr,
    }

    return render(request, 'mine_mgt/admin/add_payment.html', context)


@login_required
def claims_on_offer(request):
    claims = Claim.forfeited.all()

    context = {
        'claims': claims
    }

    return render(request, 'mine_mgt/miner/claims_on_offer.html', context)


@login_required
def declined(request, id):
    claim = Claim.pending_approval.get(id=id)
    claim.status = 'declined'
    claim.save()
    return redirect('mine_mgt:dashboard')



@login_required
def add_annual_inspection(request):
    if request.method == 'POST':
        form = AnnualInspectionForm(data=request.POST)
        if form.is_valid():
            new_inspection = form.save(commit=False)
            new_inspection.save()
            if new_inspection.desicion == 'Forfeit':
                claim = new_inspection.claim
                claim.status = 'forfeit'
                claim.save()
            return redirect('mine_mgt:dashboard')
    else:
        form = AnnualInspectionForm()

    context = {
        'form': form,
    }

    return render(request, 'mine_mgt/admin/add_annual_inspection.html', context)



@login_required
def annual_inspections(request):
    if request.user.is_mine:
        obj = AnnualInspection.objects.all()
        inspections = []
        for inspection in obj:
            if inspection.claim in request.user.claims.all():
                inspections.append(inspection)
        
        context = {
            'inspections': inspections,
        }

    else:
        inspections = AnnualInspection.objects.all()
        print('========================================================', inspections)
        context = {
            'inspections': inspections,
        }
    
    return render(request, 'mine_mgt/admin/annual_inspections.html', context)
